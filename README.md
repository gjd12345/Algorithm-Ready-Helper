# 🚀 算法与大厂机试备战全能系统 

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-FastAPI%20%7C%20LangChain-green.svg" alt="Framework">
  <img src="https://img.shields.io/badge/AI-DeepSeek--V3-orange.svg" alt="AI Model">
  <img src="https://img.shields.io/badge/Database-ChromaDB-red.svg" alt="Vector DB">
  <img src="https://img.shields.io/badge/Editor-Trae%20%7C%20VS%20Code-blueviolet.svg" alt="Editor Support">
</p>

---

## 🌈 欢迎使用你的“面试开挂神器”！

本项目不仅仅是一个代码仓库，而是一个集 **本地海量题库**、**极速检索 UI**、**Agentic RAG 智能助手** 与 **Obsidian 笔记生态** 于一体的备战闭环系统。专为追求高效、深度备考的算法爱好者及校招/社招同学设计。

---

## ✨ 核心亮点 (Core Features)

### 🎨 1. 极致的视觉与交互体验 (Ultimate UI/UX)
- **🌈 可视化壁纸库 (NEW!)**:
  - **Steam 自动同步**: 直接扫描 Wallpaper Engine 创意工坊目录，支持 MP4 视频、GIF 与静态预览。
  - **智能元数据提取**: 自动读取 `project.json`，在 UI 中显示壁纸的**真实标题**，告别冷冰冰的数字文件夹 ID。
  - **一键切换与关闭**: 提供可视化画廊，点击预览图即可秒换背景；支持“一键关闭背景”回归纯净渐变色。
- **🧊 沉浸式专注模式 (Focus Mode)**: 
  - **双模式切换**: 支持“突出内容”与“突出背景”两种显示状态。
  - **动态透明度**: 开启“突出背景”时，UI 元素会自动大幅透明并弱化，让你在思考时享受完美的动态视觉。
- **🧊 全面 Glassmorphism UI**: 深度应用毛玻璃（Frosted Glass）特效，配合 `backdrop-filter: blur(20px)`，界面半透明且支持背景透出，极具现代美感。
- **⚡ 毫秒级全库搜索**: 基于前端即时过滤 + 后端 BM25/向量检索，5400+ 题目瞬间触达。
- **🏢 厂牌分类筛选**: 深度提取各大厂（阿里、腾讯、字节、美团、华为等）真题，支持按公司、类别、考点一键过滤。

### 🤖 2. 深度集成的 AI 智能 Agent (DeepSeek 驱动)
- **🧠 Adaptive-RAG 智能路由**: 自动分析用户意图（如 SIMPLE_CHAT, RETRIEVE_PROBLEMS, COMPLEX_REASONING），动态调整检索策略，确保 AI 回复精准且高效。
- **💬 网页版级对话管理**: 
  - **多会话支持**: 支持开启多个独立对话 Session，历史记录左侧面板随心切换。
  - **持久化存储**: 聊天记录本地永不丢失，刷新页面即刻找回。
  - **Markdown 完美渲染**: 代码高亮、数学公式、列表排版，视觉体验比肩原生 DeepSeek。

### 📝 3. Obsidian 笔记生态闭环 (Enhanced!)
- **🔄 实时增量流式同步**: 开启“同步 Obsidian”开关后，AI 的每一句回复都会以**流式增量**形式实时写入 Obsidian 库。
- **📂 自动化目录与智能路由**: AI 会智能识别对话题目，自动将分析笔记路由到对应的分类目录（如 `LeetCode Hot100` 或 `华为机试`），实现知识库的自动化整理。

---

## 🛠️ 技术深度优化 (Engineering Excellence)

- **🚀 多线程流式服务 (Multi-threaded)**: 后端升级为 `ThreadingTCPServer`，支持高带宽视频流请求与 API 数据请求并发执行，彻底解决视频加载卡死 API 的问题。
- **🛡️ HTTP Range 请求支持**: 实现完整的 `206 Partial Content` 响应，支持浏览器对 MP4 视频的切片加载与进度拖动，极大降低内存占用。
- **🚀 异步加载架构**: RAG 向量数据库在后台线程异步初始化，服务器启动后**秒开**，无需等待 3.9 万条数据加载即可先行使用搜索与壁纸功能。
- **🛡️ Windows 文件并发处理**: 引入了临时文件重命名与重试机制，解决了 Obsidian 索引期间可能产生的文件访问冲突（Errno 13 Permission denied）。

---

## 🛠️ 技术栈 (Tech Stack)

| 模块 | 技术实现 |
| :--- | :--- |
| **后端核心** | Python 3.10+, ThreadingTCPServer |
| **AI 引擎** | DeepSeek-V3 API |
| **检索增强 (RAG)** | LangChain, ChromaDB (3.9w+ Chunks), HuggingFace Embeddings |
| **前端界面** | HTML5, Modern CSS (Glassmorphism), Vanilla JS |
| **数据处理** | Jupyter Notebooks (.ipynb), Markdown (.md), Python Scripts |

---

## 📂 目录结构预览

```text
📦 Algorithm-Ready-Helper
 ┣ 📂 src/main/python/        # 🐍 LeetCode Hot 100 经典题目的手写实现
 ┣ 📂 search_tool/            # 🚀 核心服务：本地搜索与 RAG 系统
 ┃ ┣ 📜 server.py             # 🖥️ 多线程后端：AI 逻辑、视频流代理与 Obsidian 同步
 ┃ ┣ 📜 ingest.py             # 📥 向量库构建：本地题目 Embedding 化
 ┃ ┣ 📜 index.html            # 🎨 沉浸式 UI：画廊壁纸、专注模式与 AI 对话
 ┃ ┗ 📂 chroma_db/            # 🗄️ (自动生成) Chroma 向量数据库持久化目录
 ┣ 📂 大厂笔试真题/           # 🏢 (需自行添加) 存放你的历年机试真题（.ipynb）
 ┣ 📂 大厂面试真题/           # 💬 (需自行添加) 存放面试面经与系统设计题目（.md）
 ┗ 📜 *.py                    # 🧹 各种数据抓取、清洗与重命名脚本
```

---

## 🚀 快速上手 (Quick Start)

### 1️⃣ 环境准备
建议使用 Python 3.8 或更高版本：
```bash
# 克隆或进入项目目录
cd leetcode-hot100-ACM

# 安装运行与检索依赖
pip install requests chromadb langchain-community langchain-huggingface langchain-text-splitters langchain-core sentence-transformers nbformat
```

### 2️⃣ 基础配置
编辑 [server.py]，配置你的专属环境：
```python
BASE_DIR = r"YOUR_PROJECT_PATH" 
OBSIDIAN_VAULT_PATH = r"YOUR_OBSIDIAN_VAULT_PATH"
DEEPSEEK_API_KEY = "YOUR_DEEPSEEK_API_KEY"
```

### 3️⃣ 初始化知识库 (RAG 必备)
运行脚本将本地所有题目索引至向量数据库：
```bash
python search_tool/ingest.py
```

### 4️⃣ 启动系统
```bash
python search_tool/server.py
```
访问：[http://127.0.0.1:8000](http://127.0.0.1:8000)，开启你的沉浸式高效备考之旅！

---

## 💡 备考小贴士 (Tips)
1. **🎨 背景与专注**: 累了可以点击壁纸库换个心情，思考复杂题目时开启“突出背景”模式，减少 UI 干扰。
2. **善用“发送给 AI”**: 在题目详情弹窗中，点击该按钮可快速获得 DeepSeek 的专业解答。
3. **结合 Obsidian**: 建议在刷题时开启同步开关，将 AI 的解题思路直接沉淀到 Obsidian，方便后期复习。

---

## 🤝 贡献与反馈
如果你在使用过程中有任何好的建议或发现了 Bug，欢迎提交 Issue。让我们一起把这个系统做得更好！

---
<p align="center">Made with ❤️ for Algorithmic Excellence</p>
