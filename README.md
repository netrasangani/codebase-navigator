# 🚀 Codebase Navigator

> 🤖 An Agentic RAG-based AI assistant for understanding GitHub repositories using natural-language questions.

**Codebase Navigator** is an AI-powered developer assistant that allows users to ask natural-language questions about a GitHub repository.

Instead of manually searching through a large codebase, the system analyzes the repository, creates semantic embeddings, stores them in a FAISS vector store, retrieves relevant source-code chunks, and uses a local Qwen language model to generate a grounded answer.

---

# ✨ Features

- 🔗 GitHub Repository Integration
- 🤖 Multi-Agent Architecture
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic Code Search
- 📚 Automatic Code Chunking
- 🧮 Hugging Face Embeddings
- ⚡ FAISS Vector Similarity Search
- 🛠️ Tool-Based Agent Execution
- 💬 Natural-Language Code Questions
- 🧩 Conversation Context
- 📝 Request ID Based Logging
- 🏠 Local AI Models
- ⚡ FastAPI Backend
- 🎨 React + Vite Frontend

---

# 🏗️ System Architecture

```text
                         👤 USER
                           │
                           │ GitHub URL
                           ▼
                ┌─────────────────────┐
                │   🤖 ORCHESTRATOR   │
                │        AGENT        │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  📦 REPOSITORY      │
                │      AGENT          │
                │      + TOOL         │
                └──────────┬──────────┘
                           │
                           ▼
                    🔗 CLONE REPO
                           │
                           ▼
                ┌─────────────────────┐
                │   🔬 CODE ANALYSIS  │
                │       AGENT         │
                │       + TOOL        │
                └──────────┬──────────┘
                           │
                           ▼
                   📄 READ SOURCE CODE
                           │
                           ▼
                       ✂️ CHUNKING
                           │
                           ▼
                🧠 HUGGING FACE
                   EMBEDDINGS
                           │
                           ▼
                ┌─────────────────────┐
                │   🗄️ FAISS VECTOR   │
                │       STORE         │
                └──────────┬──────────┘
                           │
                    ═══ INDEXING ═══
                           │
                           ▼
                         👤 USER
                           │
                           │ Question
                           ▼
                ┌─────────────────────┐
                │   🤖 ORCHESTRATOR   │
                │        AGENT        │
                └──────────┬──────────┘
                           │
                        RETRIEVE
                           ▼
                ┌─────────────────────┐
                │   🔎 RETRIEVAL      │
                │       AGENT         │
                │       + TOOL        │
                └──────────┬──────────┘
                           │
                           ▼
                  🔍 FAISS SEARCH
                           │
                           ▼
                📚 RELEVANT CODE
                     CHUNKS
                           │
                           ▼
                ┌─────────────────────┐
                │   🤖 ANSWER AGENT   │
                │       + QWEN        │
                └──────────┬──────────┘
                           │
                           ▼
                     💬 FINAL ANSWER
