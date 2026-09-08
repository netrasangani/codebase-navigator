# 🚀 Codebase Navigator

## 🔍 Overview

**Codebase Navigator** is an AI-powered codebase understanding system that allows developers to interact with GitHub repositories using natural language.

Instead of manually searching through large and unfamiliar repositories, users can provide a GitHub repository URL and ask questions about its source code. The system combines **Agentic AI, Retrieval-Augmented Generation (RAG), semantic search, vector embeddings, FAISS, and a local Qwen LLM** to retrieve relevant code and generate grounded answers.

---

## 🔥 Key Features

### 🤖 Agentic Codebase Understanding

- Multi-agent architecture for repository analysis and question answering.
- Orchestrator Agent coordinates the question-answering workflow.
- Repository Agent handles GitHub repository cloning.
- Code Analysis Agent processes and indexes source code.
- Retrieval Agent searches the indexed repository.
- Answer Agent generates answers using retrieved repository evidence.
- Tools provide callable operations for repository cloning, code analysis, and retrieval.

### 📚 Retrieval-Augmented Generation

- Retrieves relevant code before generating an answer.
- Adds retrieved source-code context to the LLM prompt.
- Generates answers based on the actual repository instead of relying only on general model knowledge.
- Reduces hallucination by instructing the Answer Agent to stay grounded in retrieved evidence.

### 🔎 Semantic Code Search

- Converts repository code into numerical vector embeddings.
- Uses `all-MiniLM-L6-v2` for embedding generation.
- Uses FAISS for vector similarity search.
- Retrieves semantically relevant code even when the user's wording does not exactly match the source code.

### 🧠 Local AI Answer Generation

- Uses `Qwen/Qwen2.5-0.5B-Instruct` for answer generation.
- Runs the language model locally.
- Generates concise explanations from the retrieved repository context.
- Supports repository-specific code understanding.

### 📂 Automated Repository Analysis

- Accepts a GitHub repository URL.
- Automatically clones the repository.
- Reads supported source files.
- Splits source code into smaller chunks.
- Generates embeddings.
- Creates a FAISS vector store for retrieval.

### 💬 Conversational Codebase Interaction

- Users can ask multiple questions about the indexed repository.
- Maintains recent conversation history.
- Supports follow-up questions using previous conversation context.
- Provides an interactive chat-based way to explore source code.

### 📝 Request ID Logging

- Generates a unique Request ID for each API operation.
- Tracks the execution of the agentic workflow.
- Helps trace requests through the backend.
- Stores application logs for debugging and monitoring.

### 🌐 Interactive Web Interface

- React-based frontend.
- GitHub repository URL input.
- Repository indexing status and statistics.
- Conversational question-answering interface.
- Displays AI-generated answers.
- Displays retrieved source files.
- Provides suggested questions and chat controls.

---

# 🔄 Complete Workflow

```text
                    ┌──────────────┐
                    │     USER     │
                    └──────┬───────┘
                           │
                      GitHub URL
                           │
                           ▼
                 ┌──────────────────┐
                 │  ORCHESTRATOR    │
                 │      AGENT       │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ REPOSITORY AGENT │
                 └────────┬─────────┘
                          │
                    Clone Repository
                          │
                          ▼
                 ┌──────────────────┐
                 │ CODE ANALYSIS    │
                 │      AGENT       │
                 └────────┬─────────┘
                          │
                    Read Source Code
                          │
                          ▼
                       CHUNKING
                          │
                          ▼
                HUGGING FACE EMBEDDINGS
                          │
                          ▼
                 ┌──────────────────┐
                 │      FAISS       │
                 │  VECTOR STORE    │
                 └────────┬─────────┘
                          │
                    Repository Ready
                          │
                    ═══ INDEXING ═══
                          │
                          ▼
                     USER QUESTION
                          │
                          ▼
                 ┌──────────────────┐
                 │  ORCHESTRATOR    │
                 │      AGENT       │
                 └────────┬─────────┘
                          │
                       RETRIEVE
                          │
                          ▼
                 ┌──────────────────┐
                 │ RETRIEVAL AGENT  │
                 └────────┬─────────┘
                          │
                    Retrieval Tool
                          │
                          ▼
                       FAISS
                          │
                          ▼
                 Relevant Code Chunks
                          │
                          ▼
                 ┌──────────────────┐
                 │  ORCHESTRATOR    │
                 │      AGENT       │
                 └────────┬─────────┘
                          │
                        ANSWER
                          │
                          ▼
                 ┌──────────────────┐
                 │   ANSWER AGENT   │
                 │      + QWEN      │
                 └────────┬─────────┘
                          │
                          ▼
                    FINAL ANSWER
