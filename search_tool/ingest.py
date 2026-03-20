import os
import json
import nbformat
from tqdm import tqdm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "search_tool", "chroma_db")

def load_ipynb(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
            content = ""
            for cell in nb.cells:
                if cell.cell_type == 'markdown':
                    content += cell.source + "\n\n"
                elif cell.cell_type == 'code':
                    content += "```python\n" + cell.source + "\n```\n\n"
            return content
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return ""

def load_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return ""

def ingest():
    search_dirs = [
        os.path.join(BASE_DIR, "大厂笔试真题"),
        os.path.join(BASE_DIR, "按类别的AI大厂机试"),
        os.path.join(BASE_DIR, "src", "main", "python"),
        os.path.join(BASE_DIR, "大厂面试真题")
    ]
    
    documents = []
    print("Collecting files...")
    
    for d in search_dirs:
        if not os.path.exists(d): continue
        for root, _, files in os.walk(d):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, BASE_DIR).replace('\\', '/')
                
                content = ""
                if file.endswith(".ipynb"):
                    content = load_ipynb(file_path)
                elif file.endswith((".md", ".py")):
                    content = load_text_file(file_path)
                
                if content.strip():
                    doc = Document(
                        page_content=content,
                        metadata={"source": rel_path, "title": file}
                    )
                    documents.append(doc)
    
    print(f"Found {len(documents)} documents. Splitting into chunks...")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    
    print(f"Created {len(chunks)} chunks. Initializing Vector Store...")
    
    # Using a lightweight local embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Create and persist vector store
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    print(f"Successfully indexed {len(chunks)} chunks into {PERSIST_DIRECTORY}")

if __name__ == "__main__":
    ingest()
