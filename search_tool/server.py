import os
import json
import http.server
import socketserver
import threading
import webbrowser
import urllib.parse
import subprocess
import shutil
import requests
import math
import re
import datetime
import time
import mimetypes
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 彻底禁用 HuggingFace 联网检查，避免首次检索时的网络超时卡顿
os.environ["HF_HUB_OFFLINE"] = "1"

try:
    from mcp.server.fastmcp import FastMCP
except Exception:
    FastMCP = None

# Define the base directory globally for accessibility
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "search_tool", "chroma_db")
# 使用原始字符串定义路径，避免编码和转义问题
OBSIDIAN_VAULT_PATH = os.environ.get("OBSIDIAN_VAULT_PATH", "")
# API Configuration
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "your-api-key-here")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Global Model Selection
CURRENT_MODEL = "deepseek-chat"

# Global vector store instance
VECTOR_DB = None
BM25_INDEX = None
BM25_DOCS = None
PROBLEM_MAP = {} # 新增：用于快速查找题目分类的映射表

def _tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]", (text or "").lower())

def _build_bm25_index(docs: list[str]):
    inv = {}
    doc_len = []
    df = {}
    for doc_id, content in enumerate(docs):
        tokens = _tokenize(content)
        doc_len.append(len(tokens))
        tf = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1
        for t, c in tf.items():
            inv.setdefault(t, []).append((doc_id, c))
            df[t] = df.get(t, 0) + 1
    n = len(docs)
    avgdl = (sum(doc_len) / n) if n else 0.0
    return {
        "inv": inv,
        "df": df,
        "doc_len": doc_len,
        "avgdl": avgdl,
        "n": n,
        "k1": 1.5,
        "b": 0.75,
    }

def _bm25_search(query: str, top_k: int) -> list[int]:
    if not BM25_INDEX:
        return []
    q_tokens = _tokenize(query)
    if not q_tokens:
        return []

    inv = BM25_INDEX["inv"]
    df = BM25_INDEX["df"]
    doc_len = BM25_INDEX["doc_len"]
    avgdl = BM25_INDEX["avgdl"] or 1.0
    n = BM25_INDEX["n"] or 1
    k1 = BM25_INDEX["k1"]
    b = BM25_INDEX["b"]

    candidates = set()
    for t in q_tokens:
        postings = inv.get(t)
        if postings:
            for doc_id, _ in postings:
                candidates.add(doc_id)

    scores = {}
    for t in q_tokens:
        postings = inv.get(t)
        if not postings:
            continue
        n_q = df.get(t, 0)
        idf = math.log(1.0 + (n - n_q + 0.5) / (n_q + 0.5))
        for doc_id, tf in postings:
            dl = doc_len[doc_id] or 1
            denom = tf + k1 * (1 - b + b * dl / avgdl)
            score = idf * (tf * (k1 + 1)) / (denom or 1.0)
            scores[doc_id] = scores.get(doc_id, 0.0) + score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [doc_id for doc_id, _ in ranked[:top_k]]

def _rrf_fuse(lists: list[list[int]], k: int = 60) -> list[int]:
    fused = {}
    for lst in lists:
        for rank, doc_id in enumerate(lst, start=1):
            fused[doc_id] = fused.get(doc_id, 0.0) + 1.0 / (k + rank)
    return [doc_id for doc_id, _ in sorted(fused.items(), key=lambda x: x[1], reverse=True)]

def retrieve_documents(query: str, top_k: int) -> list[dict]:
    global BM25_DOCS
    doc_indices = []
    
    # 1. 标题启发式增强：如果查询中包含某些关键词，先在文件名中找匹配
    title_boost_docs = []
    query_lower = query.lower()
    
    # 提取查询中的潜在关键词（如：公司名、算法名）
    potential_keywords = [k for k in query_lower.split() if len(k) > 1]
    # 额外增加常见大厂关键词匹配
    companies = ["华为", "腾讯", "字节", "阿里", "美团", "百度", "京东", "快手", "拼多多", "网易", "滴滴", "携程", "小米", "小红书"]
    found_companies = [c for c in companies if c in query_lower]
    
    boost_count = 0
    if BM25_DOCS:
        for i, m in enumerate(BM25_DOCS["metadatas"]):
            source = m.get("source", "").lower()
            # 如果文件名包含查询中的公司名，给予极高权重
            if any(c.lower() in source for c in found_companies):
                title_boost_docs.append(i)
                boost_count += 1
            if boost_count > 10: break # 最多提取10个标题匹配

    if VECTOR_DB:
        try:
            vector_docs = VECTOR_DB.similarity_search(query, k=max(top_k, 10))
            vec_indices = []
            if BM25_DOCS is not None:
                for d in vector_docs:
                    source = d.metadata.get("source")
                    if source is None:
                        continue
                    for i, m in enumerate(BM25_DOCS["metadatas"]):
                        if m.get("source") == source:
                            vec_indices.append(i)
                            break
            doc_indices.append(vec_indices)
        except Exception:
            doc_indices.append([])

    if BM25_INDEX:
        doc_indices.append(_bm25_search(query, top_k=max(top_k, 10)))
    
    # 将标题增强的结果放在最前面
    if title_boost_docs:
        doc_indices.append(title_boost_docs)

    fused = _rrf_fuse(doc_indices)[:top_k] if doc_indices else []
    
    if not fused and VECTOR_DB:
        vector_docs = VECTOR_DB.similarity_search(query, k=top_k)
        return [{"source": d.metadata.get("source", "Unknown"), "content": d.page_content} for d in vector_docs]

    results = []
    if BM25_DOCS is None:
        return results
    for idx in fused:
        m = BM25_DOCS["metadatas"][idx] or {}
        c = BM25_DOCS["documents"][idx] or ""
        results.append({"source": m.get("source", "Unknown"), "content": c})
    return results

def init_vector_db():
    global VECTOR_DB, BM25_INDEX, BM25_DOCS
    if os.path.exists(PERSIST_DIRECTORY):
        print("Loading Vector DB for RAG...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        VECTOR_DB = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
        
        print("Initializing Hybrid Search (BM25 + Vector + RRF)...")
        try:
            # Fix "too many SQL variables" by fetching in batches
            all_metadatas = []
            all_documents = []
            
            # First, get total count
            collection = VECTOR_DB._collection
            total_count = collection.count()
            print(f"Total documents in Vector DB: {total_count}")
            
            # Fetch in batches of 1000
            batch_size = 500
            for i in range(0, total_count, batch_size):
                batch = collection.get(
                    limit=batch_size,
                    offset=i,
                    include=["metadatas", "documents"]
                )
                if batch["metadatas"]:
                    all_metadatas.extend(batch["metadatas"])
                if batch["documents"]:
                    all_documents.extend(batch["documents"])
                print(f"Loaded {len(all_documents)} / {total_count} documents...")

            BM25_DOCS = {
                "metadatas": all_metadatas,
                "documents": all_documents
            }
            
            if all_documents:
                BM25_INDEX = _build_bm25_index(all_documents)
                print("Hybrid Search initialized successfully with all documents.")
            else:
                print("No documents found for Hybrid Search initialization.")
        except Exception as e:
            import traceback
            print(f"Error initializing Hybrid Search: {e}")
            traceback.print_exc()
            
        print("Vector DB loaded successfully.")
    else:
        print("Vector DB not found. RAG will be disabled.")

def generate_problems_json():
    global PROBLEM_MAP
    # Include all specified directories
    search_dirs = [
        os.path.join(BASE_DIR, "大厂笔试真题"),
        os.path.join(BASE_DIR, "按类别的AI大厂机试"),
        os.path.join(BASE_DIR, "src", "main", "python"), # leetcodehot100 ACM (converted)
        os.path.join(BASE_DIR, "大厂面试真题")
    ]
    
    problems = []
    seen_paths = set()
    
    for d in search_dirs:
        if not os.path.exists(d):
            continue
            
        is_ai_dir = "按类别的AI大厂机试" in d
        
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith((".ipynb", ".py", ".md")):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, BASE_DIR).replace('\\', '/')
                    
                    if rel_path in seen_paths:
                        continue
                        
                    seen_paths.add(rel_path)
                    
                    # Heuristic for AI tagging
                    is_ai = is_ai_dir or any(k in file.lower() for k in ["ai", "机器学习", "深度学习", "卷积", "神经网络", "transformer", "attention"])
                    
                    # Extract company information
                    company = "其他"
                    companies = {
                        "阿里": ["阿里", "Alibaba", "淘天", "蚂蚁"],
                        "腾讯": ["腾讯", "Tencent", "微信"],
                        "字节": ["字节", "ByteDance", "抖音", "飞书"],
                        "美团": ["美团", "Meituan"],
                        "百度": ["百度", "Baidu"],
                        "京东": ["京东", "JD"],
                        "华为": ["华为", "Huawei"],
                        "网易": ["网易", "NetEase"],
                        "滴滴": ["滴滴", "Didi"],
                        "携程": ["携程", "Ctrip"],
                        "拼多多": ["拼多多", "PDD"],
                        "小米": ["小米", "Xiaomi"],
                        "小红书": ["小红书", "Xiaohongshu", "Red"],
                        "快手": ["快手", "Kuaishou"],
                        "微软": ["微软", "Microsoft"],
                        "谷歌": ["谷歌", "Google"],
                        "亚马逊": ["亚马逊", "Amazon"]
                    }
                    
                    for c_name, keywords in companies.items():
                        if any(k.lower() in rel_path.lower() for k in keywords):
                            company = c_name
                            break

                    category = "其他"
                    if "大厂笔试真题" in rel_path: category = "笔试真题"
                    elif "大厂面试真题" in rel_path: category = "面试真题"
                    elif "python" in rel_path: category = "LeetCode Hot100"
                    elif "按类别的AI" in rel_path: category = "AI专项"

                    prob = {
                        "name": file,
                        "path": rel_path,
                        "isAI": is_ai,
                        "category": category,
                        "company": company
                    }
                    problems.append(prob)
                    # 将题目名称（不含后缀）映射到分类，用于快速同步定位
                    short_name = file.replace('.ipynb','').replace('.py','').replace('.md','')
                    PROBLEM_MAP[short_name] = category
    
    with open(os.path.join(os.path.dirname(__file__), 'problems.json'), 'w', encoding='utf-8') as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)
    
    print(f"Generated problems.json with {len(problems)} entries.")

if FastMCP:
    mcp_server = FastMCP("LeetCode-RAG-Agent")

    @mcp_server.tool()
    def search_problems(query: str, complexity: str = "medium") -> str:
        if not VECTOR_DB:
            return "Search database not initialized."
        top_k = 5 if complexity == "complex" else 3
        refs = retrieve_documents(query, top_k=top_k)
        return "\n---\n".join([f"Source: {r['source']}\nContent: {r['content']}" for r in refs])

    @mcp_server.resource("prompt://system_prompt")
    def get_system_prompt() -> str:
        return "You are a helpful assistant for LeetCode problems."

    def start_mcp_server_thread():
        try:
            print("MCP Server defined. To run independently: 'mcp run search_tool.server:mcp_server'")
        except Exception as e:
            print(f"Failed to start MCP server: {e}")
else:
    mcp_server = None

def call_llm(messages, model=None, stream=False):
    """Unified LLM Caller"""
    model_name = model or CURRENT_MODEL
    api_key = DEEPSEEK_API_KEY
    base_url = DEEPSEEK_BASE_URL
    
    try:
        return requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model_name,
                "messages": messages,
                "stream": stream,
                "temperature": 0
            },
            timeout=60,
            stream=stream
        )
    except Exception as e:
        print(f"LLM Call Error: {e}")
        raise e

def get_query_intent(query):
    """Adaptive-RAG Router: Classify query complexity and intent"""
    try:
        response = call_llm([
             {"role": "system", "content": """你是一个智能查询路由助手。请分析用户查询的复杂度和意图，并返回以下分类之一：

1. SIMPLE_CHAT: 简单的打招呼、感谢或不需要外部知识的一般性对话。（无需检索）
2. RETRIEVE_PROBLEMS: 用户在寻找具体的编程题、机试题或代码实现。（需要检索题库）
3. RETRIEVE_INTERVIEW: 用户在查询面试经验、面试指南、系统设计等面经内容。（需要检索面经）
4. RETRIEVE_AI: 用户在查询AI、机器学习算法、手撕AI相关内容。（需要检索AI资料）
5. COMPLEX_REASONING: 需要多步推理、代码生成或深度分析的复杂问题。（需要 Agent 模式 + 检索）

只需返回分类关键词（如：COMPLEX_REASONING），不要返回其他内容。"""},
             {"role": "user", "content": query}
        ])
        intent = response.json()['choices'][0]['message']['content'].strip()
        print(f"Adaptive-RAG Router Intent: {intent}")
        return intent if intent in ["SIMPLE_CHAT", "RETRIEVE_PROBLEMS", "RETRIEVE_INTERVIEW", "RETRIEVE_AI", "COMPLEX_REASONING"] else "SIMPLE_CHAT"
    except Exception as e:
        print(f"Router Error: {e}")
        return "SIMPLE_CHAT"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        super().end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path.rstrip('/')
        if not path: path = '/'
        
        print(f"DEBUG: [GET] {path}")

        if path in ['/', '/index.html']:
            try:
                index_path = os.path.join(os.path.dirname(__file__), 'index.html')
                with open(index_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
            return

        if path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return

        if path == '/open':
            query = urllib.parse.parse_qs(parsed_url.query)
            rel_path = query.get('path', [None])[0]
            preferred_ide = query.get('ide', [None])[0]
            
            if rel_path:
                abs_path = os.path.normpath(os.path.join(BASE_DIR, rel_path))
                if os.path.exists(abs_path):
                    try:
                        opener = None
                        candidates = []
                        if preferred_ide in ['code', 'trae']:
                            candidates.append(preferred_ide)
                            for c in ['code', 'trae']:
                                if c not in candidates:
                                    candidates.append(c)

                        for candidate in candidates:
                            resolved = shutil.which(candidate)
                            if resolved:
                                opener = resolved
                                break

                        opened_via = None
                        if opener:
                            opened_via = os.path.basename(opener)
                        else:
                            opened_via = 'startfile'

                        def _launch():
                            try:
                                if opener:
                                    opener_base = os.path.basename(opener).lower()
                                    if opener_base.startswith('code'):
                                        user_data_dir = os.path.join(BASE_DIR, '.vscode-userdata')
                                        extensions_dir = os.path.join(BASE_DIR, '.vscode-extensions')
                                        os.makedirs(user_data_dir, exist_ok=True)
                                        os.makedirs(extensions_dir, exist_ok=True)
                                        subprocess.Popen(
                                            [
                                                opener,
                                                '--reuse-window',
                                                '--user-data-dir',
                                                user_data_dir,
                                                '--extensions-dir',
                                                extensions_dir,
                                                abs_path,
                                            ],
                                            shell=False,
                                        )
                                    else:
                                        subprocess.Popen([opener, abs_path], shell=False)
                                else:
                                    os.startfile(abs_path)
                            except Exception as e:
                                print(f"Open file failed: {abs_path} -> {e}")

                        threading.Thread(target=_launch, daemon=True).start()

                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "status": "success",
                            "opened_via": opened_via,
                            "path": rel_path,
                        }).encode('utf-8'))
                    except Exception as e:
                        self.send_response(500)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "status": "error",
                            "error": str(e),
                            "path": rel_path,
                        }).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "status": "error",
                        "error": "File not found",
                        "path": rel_path,
                    }).encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "error",
                    "error": "Missing path parameter",
                }).encode('utf-8'))
            return

        elif path == '/get_description':
            query = urllib.parse.parse_qs(parsed_url.query)
            rel_path = query.get('path', [None])[0]
            
            if rel_path:
                abs_path = os.path.normpath(os.path.join(BASE_DIR, rel_path))
                if os.path.exists(abs_path):
                    try:
                        content = ""
                        if abs_path.endswith(".ipynb"):
                            with open(abs_path, 'r', encoding='utf-8') as f:
                                nb = json.load(f)
                                for cell in nb.get('cells', []):
                                    if cell.get('cell_type') == 'markdown':
                                        content += "".join(cell.get('source', [])) + "\n\n"
                                    if len(content) > 500: break 
                        elif abs_path.endswith((".md", ".py")):
                            with open(abs_path, 'r', encoding='utf-8') as f:
                                content = f.read(2000)
                        
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/plain; charset=utf-8')
                        self.end_headers()
                        self.wfile.write(content.encode('utf-8'))
                    except Exception as e:
                        self.send_response(500)
                        self.end_headers()
                        self.wfile.write(str(e).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"File not found")
            else:
                self.send_response(400)
                self.end_headers()
            return

        elif path == '/kb_stats':
            if VECTOR_DB:
                try:
                    total_chunks = VECTOR_DB._collection.count()
                    sources = set([m.get('source') for m in VECTOR_DB.get()['metadatas'] if m.get('source')])
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "total_chunks": total_chunks,
                        "total_docs": len(sources)
                    }).encode())
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(str(e).encode())
            else:
                self.send_response(503)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Vector DB is still loading..."}).encode())
            return

        elif path == '/kb_search':
            query_params = urllib.parse.parse_qs(parsed_url.query)
            q = query_params.get('q', [''])[0]
            if VECTOR_DB and q:
                try:
                    results = VECTOR_DB.similarity_search(q, k=5)
                    formatted_results = [
                        {"source": doc.metadata.get('source'), "content": doc.page_content, "title": doc.metadata.get('title')} 
                        for doc in results
                    ]
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(formatted_results).encode())
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(str(e).encode())
            else:
                self.send_response(503)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Vector DB is still loading..."}).encode())
            return

        elif path == '/list_wallpapers':
            steam_path = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\431960"
            wallpapers = []
            try:
                if os.path.exists(steam_path):
                    for folder in os.listdir(steam_path):
                        folder_path = os.path.join(steam_path, folder)
                        if os.path.isdir(folder_path):
                            project_json_path = os.path.join(folder_path, "project.json")
                            title = folder
                            preview_file = None
                            content_file = None
                            
                            if os.path.exists(project_json_path):
                                try:
                                    with open(project_json_path, 'r', encoding='utf-8') as f:
                                        pj = json.load(f)
                                        title = pj.get('title', folder)
                                        preview_file = pj.get('preview')
                                        content_file = pj.get('file')
                                except: pass
                            
                            files = os.listdir(folder_path)
                            if not content_file:
                                content_file = next((f for f in files if f.lower().endswith('.mp4')), None)
                            if not content_file:
                                content_file = next((f for f in files if f.lower().endswith(('.gif', '.jpg', '.jpeg', '.png'))), None)
                            
                            if not preview_file:
                                preview_file = next((f for f in files if f.lower().endswith(('.gif', '.jpg', '.jpeg', '.png'))), content_file)
                            
                            if content_file:
                                is_video = content_file.lower().endswith('.mp4')
                                wallpapers.append({
                                    "id": folder,
                                    "title": title,
                                    "path": os.path.join(folder_path, content_file).replace('\\', '/'),
                                    "preview": os.path.join(folder_path, preview_file).replace('\\', '/') if preview_file else os.path.join(folder_path, content_file).replace('\\', '/'),
                                    "type": "video" if is_video else "image"
                                })
                    wallpapers.sort(key=lambda x: x['id'], reverse=True)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(wallpapers).encode())
            except Exception as e:
                import traceback
                print(f"ERROR: [LIST_WALLPAPERS] {e}\n{traceback.format_exc()}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        elif path == '/get_wallpaper':
            query_params = urllib.parse.parse_qs(parsed_url.query)
            wallpaper_path = query_params.get('path', [None])[0]
            if wallpaper_path:
                wallpaper_path = os.path.normpath(wallpaper_path.strip('"\''))
                if os.path.exists(wallpaper_path):
                    try:
                        file_size = os.path.getsize(wallpaper_path)
                        content_type, _ = mimetypes.guess_type(wallpaper_path)
                        if not content_type:
                            ext = os.path.splitext(wallpaper_path)[1].lower()
                            mimes = {
                                '.mp4': 'video/mp4',
                                '.gif': 'image/gif',
                                '.jpg': 'image/jpeg',
                                '.jpeg': 'image/jpeg',
                                '.png': 'image/png',
                                '.webp': 'image/webp'
                            }
                            content_type = mimes.get(ext, 'application/octet-stream')
                        
                        range_header = self.headers.get('Range')
                        start = 0
                        end = file_size - 1
                        
                        if range_header and range_header.startswith('bytes='):
                            try:
                                byte_range = range_header.replace('bytes=', '')
                                parts = byte_range.split('-')
                                if parts[0]: start = int(parts[0])
                                if len(parts) > 1 and parts[1]: end = int(parts[1])
                            except: pass
                        
                        if start >= file_size: start = file_size - 1
                        if end >= file_size: end = file_size - 1
                        if end < start: end = start
                        content_length = end - start + 1
                        
                        if range_header:
                            self.send_response(206)
                            self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
                        else:
                            self.send_response(200)
                        
                        self.send_header('Content-Type', content_type)
                        self.send_header('Content-Length', str(content_length))
                        self.send_header('Accept-Ranges', 'bytes')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('X-Content-Type-Options', 'nosniff')
                        self.end_headers()
                        
                        with open(wallpaper_path, 'rb') as f:
                            f.seek(start)
                            remaining = content_length
                            while remaining > 0:
                                chunk_size = min(remaining, 256 * 1024)
                                chunk = f.read(chunk_size)
                                if not chunk: break
                                try:
                                    self.wfile.write(chunk)
                                    remaining -= len(chunk)
                                except:
                                    break
                        return
                    except Exception as e:
                        print(f"[WALLPAPER] Error: {e}")
                else:
                    self.send_response(404)
                    self.end_headers()
            else:
                self.send_response(400)
                self.end_headers()
            return

        else:
            super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            messages = data.get('messages', [])
            
            # Adaptive-RAG Routing
            references = []
            intent = "SIMPLE_CHAT"
            if VECTOR_DB and messages:
                last_user_message = next((m['content'] for m in reversed(messages) if m['role'] == 'user'), None)
                if last_user_message:
                    intent = get_query_intent(last_user_message)
                    
                    if intent != "SIMPLE_CHAT":
                        print(f"Executing Targeted Retrieval for intent: {intent}")
                        
                        # 大幅增加检索视野，让 AI 能参考更多题目
                        top_k = 20 if intent == "COMPLEX_REASONING" else 12
                        references = retrieve_documents(last_user_message, top_k=top_k)
                        context = "\n---\n".join([f"Source: {r['source']}\nContent: {r['content']}" for r in references])
                        
                        # 获取题库统计信息用于 Prompt
                        total_count = len(PROBLEM_MAP)
                        companies_count = len(set([p.get('company', '其他') for p in PROBLEM_MAP.values() if isinstance(p, dict)])) # This logic needs fixing as PROBLEM_MAP values are strings
                        
                        # 修正：从内存中获取分类和公司概况
                        try:
                            with open(os.path.join(BASE_DIR, "search_tool", "problems.json"), 'r', encoding='utf-8') as pf:
                                all_probs = json.load(pf)
                                total_count = len(all_probs)
                                cats = set([p['category'] for p in all_probs])
                                comps = set([p['company'] for p in all_probs if p['company'] != "其他"])
                                repo_summary = f"当前本地库共包含 {total_count} 道题目，涵盖 {len(cats)} 个分类及 {len(comps)} 家大厂（如 {', '.join(list(comps)[:8])}...）的真题。"
                        except:
                            repo_summary = "当前本地库包含 5000+ 道大厂面试/笔试真题。"

                        # Branching System Prompts based on Adaptive Router
                        prompt_templates = {
                            "RETRIEVE_PROBLEMS": f"你是一个顶尖算法专家。你拥有访问本地全量题库（{total_count}道题目）的权限。\n{repo_summary}\n\n用户正在咨询题目，请参考以下检索到的最相关的参考内容进行深度分析，提供最优解法及符合 ACM 模式的 Python 代码：\n\n【本地参考内容】:\n{context}",
                            "RETRIEVE_INTERVIEW": f"你是一个大厂资深面试官。你拥有访问本地全量面经库的权限。\n{repo_summary}\n\n请参考以下检索到的面试资料，为用户提供精准的建议或系统设计思路：\n\n【本地参考内容】:\n{context}",
                            "RETRIEVE_AI": f"你是一个 AI 算法专家。你拥有访问本地 AI 专项题库的权限。\n{repo_summary}\n\n请参考以下检索到的资料进行专业解答：\n\n【本地参考内容】:\n{context}",
                            "COMPLEX_REASONING": f"""你是一个高级推理 Agent。你正在管理一个包含 {total_count} 道题目的本地知识库。
{repo_summary}

请综合以下检索到的多方资料，进行跨维度的深度分析和推理。
【综合参考资料】:
{context}"""
                        }
                        
                        system_prompt = {
                            "role": "system",
                            "content": prompt_templates.get(intent, "你是一个全能的面试专家。")
                        }
                        
                        if messages[0]['role'] == 'system':
                            messages[0] = system_prompt
                        else:
                            messages.insert(0, system_prompt)
                    else:
                        print("Adaptive-RAG: Skipping retrieval for simple chat.")
            
            try:
                # Use stream=True for real-time response
                response = call_llm(messages, stream=True)
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.send_header('Cache-Control', 'no-cache')
                self.send_header('Connection', 'keep-alive')
                self.end_headers()

                # Send references first as a special event
                if references:
                    ref_data = json.dumps({"type": "references", "data": references})
                    self.wfile.write(f"data: {ref_data}\n\n".encode())
                    self.wfile.flush()

                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith('data: '):
                            self.wfile.write((decoded_line + "\n\n").encode())
                            self.wfile.flush()
                            
            except Exception as e:
                print(f"Chat API Error: {e}")
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode())
        elif parsed_url.path == '/sync_category':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            category_name = data.get('category', '我的刷题笔记')
            problems = data.get('problems', [])
            
            try:
                # Ensure the target directory in Obsidian exists
                obsidian_dir = os.path.join(OBSIDIAN_VAULT_PATH, "大厂面试笔试")
                os.makedirs(obsidian_dir, exist_ok=True)
                
                # Generate filename
                safe_cat_name = re.sub(r'[\\/:*?"<>|]', '_', category_name)
                note_file = os.path.normpath(os.path.join(obsidian_dir, f"{safe_cat_name}.md"))
                
                # Write to a temporary file first, then rename to avoid locking issues on Windows
                temp_file = note_file + ".tmp"
                
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {category_name}\n\n")
                    f.write(f"**同步时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"**题目总数**: {len(problems)}\n\n---\n\n")
                    
                    for p in problems:
                        title = p['name'].replace('.ipynb', '').replace('.py', '').replace('.md', '')
                        f.write(f"## {title}\n")
                        f.write(f"- **分类**: {p.get('category', '未分类')}\n")
                        f.write(f"- **路径**: `{p['path']}`\n")
                        
                        # Try to get description if possible
                        abs_path = os.path.normpath(os.path.join(BASE_DIR, p['path']))
                        desc = ""
                        if os.path.exists(abs_path):
                            try:
                                if abs_path.endswith(".ipynb"):
                                    with open(abs_path, 'r', encoding='utf-8') as nbf:
                                        nb = json.load(nbf)
                                        for cell in nb.get('cells', []):
                                            if cell.get('cell_type') == 'markdown':
                                                desc += "".join(cell.get('source', [])) + "\n"
                                                if len(desc) > 300: break # Keep summary short
                                elif abs_path.endswith((".md", ".py")):
                                    with open(abs_path, 'r', encoding='utf-8') as tf:
                                        desc = tf.read(300)
                            except Exception:
                                pass
                                    
                        if desc:
                            f.write(f"\n> {desc.strip()}\n\n")
                        
                        f.write(f"[在 Trae 中打开此题目](http://localhost:8000/open?path={urllib.parse.quote(p['path'])})\n\n---\n\n")
                
                # Atomic replace (as much as possible on Windows)
                if os.path.exists(note_file):
                    try:
                        os.remove(note_file)
                    except OSError:
                        # If removal fails, try a few times or ignore
                        time.sleep(0.1)
                        os.remove(note_file)
                os.rename(temp_file, note_file)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "file": note_file}).encode())
                
            except Exception as e:
                import traceback
                print(f"Error syncing to Obsidian: {traceback.format_exc()}")
                self.send_response(500)
                self.end_headers()
                error_msg = str(e)
                if "[Errno 13]" in error_msg:
                    error_msg = f"权限不足或文件被占用 (请检查是否在 Obsidian 中打开了该文件): {error_msg}"
                self.wfile.write(json.dumps({"error": error_msg}).encode())
        elif parsed_url.path == '/sync_single':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            p = json.loads(post_data.decode('utf-8'))
            
            try:
                # Ensure the target directory in Obsidian exists
                obsidian_dir = os.path.join(OBSIDIAN_VAULT_PATH, "大厂面试笔试")
                os.makedirs(obsidian_dir, exist_ok=True)
                
                title = p['name'].replace('.ipynb', '').replace('.py', '').replace('.md', '')
                safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)
                note_file = os.path.normpath(os.path.join(obsidian_dir, f"{safe_title}.md"))
                
                # Use temporary file to avoid locking
                temp_file = note_file + ".tmp"
                
                # Get full description
                abs_path = os.path.normpath(os.path.join(BASE_DIR, p['path']))
                desc = ""
                if os.path.exists(abs_path):
                    try:
                        if abs_path.endswith(".ipynb"):
                            with open(abs_path, 'r', encoding='utf-8') as nbf:
                                nb = json.load(nbf)
                                for cell in nb.get('cells', []):
                                    if cell.get('cell_type') == 'markdown':
                                        desc += "".join(cell.get('source', [])) + "\n"
                        elif abs_path.endswith((".md", ".py")):
                            with open(abs_path, 'r', encoding='utf-8') as tf:
                                desc = tf.read()
                    except Exception as e:
                        print(f"Error reading file for Obsidian sync: {e}")
                        desc = f"读取文件失败: {str(e)}"
                else:
                    desc = "文件不存在或路径错误。"

                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {title}\n\n")
                    f.write(f"- **分类**: {p.get('category', '未分类')}\n")
                    f.write(f"- **本地路径**: `{p['path']}`\n\n")
                    f.write(f"## 题目描述\n\n{desc}\n\n")
                    f.write(f"---\n")
                    f.write(f"[在 Trae 中打开此题目](http://localhost:8000/open?path={urllib.parse.quote(p['path'])})\n")
                
                # Handle existing file replacement
                if os.path.exists(note_file):
                    try:
                        os.remove(note_file)
                    except OSError:
                        time.sleep(0.1)
                        os.remove(note_file)
                os.rename(temp_file, note_file)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "file": note_file}).encode())
                
            except Exception as e:
                import traceback
                print(f"Error syncing single problem: {traceback.format_exc()}")
                self.send_response(500)
                self.end_headers()
                error_msg = str(e)
                if "[Errno 13]" in error_msg:
                    error_msg = f"权限不足或文件被占用 (请检查是否在 Obsidian 中打开了该文件): {error_msg}"
                self.wfile.write(json.dumps({"error": error_msg}).encode())
        elif parsed_url.path == '/sync_chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            title = data.get('title', 'AI 对话')
            messages = data.get('messages', [])
            
            try:
                # 智能识别同步路径：如果是针对特定题目的分析，尝试同步到题目对应的笔记中
                target_dir = "AI 对话"
                filename = f"{re.sub(r'[\\/:*?\"<>|]', '_', title)}.md"
                
                # 检查标题是否包含题目关键词，如果有，尝试定位到原题目文件夹
                match = re.search(r'《(.*?)》', title)
                if match:
                    problem_name = match.group(1)
                    # 使用内存中的 PROBLEM_MAP 快速定位
                    if problem_name in PROBLEM_MAP:
                        target_dir = PROBLEM_MAP[problem_name]
                        filename = f"{re.sub(r'[\\\\/:*?\"<>|]', '_', problem_name)}.md"
                    else:
                        # 模糊匹配
                        for p_name, cat in PROBLEM_MAP.items():
                            if problem_name in p_name or p_name in problem_name:
                                target_dir = cat
                                filename = f"{re.sub(r'[\\\\/:*?\"<>|]', '_', p_name)}.md"
                                break

                obsidian_dir = os.path.normpath(os.path.join(OBSIDIAN_VAULT_PATH, target_dir))
                if not os.path.exists(obsidian_dir):
                    os.makedirs(obsidian_dir, exist_ok=True)
                
                note_file = os.path.join(obsidian_dir, filename)
                temp_file = note_file + ".tmp"
                
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {title}\n\n")
                    f.write(f"**同步时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("---\n\n")
                    
                    for msg in messages:
                        role = "👤 用户" if msg['role'] == 'user' else "🤖 AI"
                        f.write(f"## {role}\n\n")
                        # 确保内容中的换行符在 Obsidian 中能正确显示
                        content = msg['content']
                        # 简单的格式美化：确保代码块前后有空行
                        content = re.sub(r'([^\\n])```', r'\1\n\n```', content)
                        content = re.sub(r'```([^\\n])', r'```\n\n\1', content)
                        f.write(f"{content}\n\n")
                        f.write("---\n\n")
                
                # 原子替换
                if os.path.exists(note_file):
                    try: os.remove(note_file)
                    except OSError:
                        time.sleep(0.1)
                        try: 
                            os.remove(note_file)
                        except: pass
                
                if os.path.exists(temp_file):
                    os.rename(temp_file, note_file)
                    print(f"Successfully synced chat to: {note_file}")
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
            except Exception as e:
                print(f"Sync Chat Error: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def start_server(port=8000):
    socketserver.TCPServer.allow_reuse_address = True
    # Bind to 0.0.0.0 and use ThreadingTCPServer for concurrent requests
    with ThreadingTCPServer(("0.0.0.0", port), Handler) as httpd:
        print(f"Serving at http://localhost:{port} (Multi-threaded)")
        threading.Timer(1.5, lambda: webbrowser.open(f"http://localhost:{port}")).start()
        httpd.serve_forever()

if __name__ == "__main__":
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    generate_problems_json()
    
    # Initialize RAG vector store in background to avoid blocking server start
    threading.Thread(target=init_vector_db, daemon=True).start()
    
    print("Starting local search server with DeepSeek AI support (RAG Enabled)...")
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nServer stopped.")
