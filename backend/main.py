import logging
import os
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.orchestrator import CodebaseOrchestrator
from agents.tools import set_vector_store
from context import clear_context, add_message, get_context


# --------------------------------------------------
# Logging setup
# --------------------------------------------------

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# FastAPI setup
# --------------------------------------------------

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Application objects
# --------------------------------------------------

orchestrator = CodebaseOrchestrator()

vector_store = None

repo_stats = {
    "files": 0,
    "chunks": 0,
    "embedding_model": "all-MiniLM-L6-v2"
}


# --------------------------------------------------
# Request models
# --------------------------------------------------

class RepoRequest(BaseModel):
    url: str


class QuestionRequest(BaseModel):
    question: str


# --------------------------------------------------
# Home route
# --------------------------------------------------

@app.get("/")
def home():

    logger.info(
        "Request ID: HOME | Home endpoint accessed"
    )

    return {
        "message": "Codebase Navigator is running!"
    }


# --------------------------------------------------
# Repository indexing
# --------------------------------------------------

@app.post("/repository")
def index_repository(request: RepoRequest):

    global vector_store
    global repo_stats

    request_id = f"REQ-{uuid.uuid4().hex[:8]}"

    logger.info(
        "Request ID: %s | Repository indexing started: %s",
        request_id,
        request.url
    )

    clear_context()

    try:

        result = orchestrator.index_repository(
            request.url,
            request_id
        )

        vector_store = result["vector_store"]

        # Make the vector store available to the tools
        set_vector_store(vector_store)

        repo_stats = {
            "files": result["files"],
            "chunks": result["chunks"],
            "embedding_model": "all-MiniLM-L6-v2"
        }

        logger.info(
            "Request ID: %s | Repository indexed successfully | Files: %s | Chunks: %s",
            request_id,
            result["files"],
            result["chunks"]
        )

        return {
            "message": "Repository indexed successfully",
            "stats": repo_stats,
            "request_id": request_id
        }

    except Exception as e:

        logger.error(
            "Request ID: %s | Repository indexing failed: %s",
            request_id,
            str(e)
        )

        return {
            "error": str(e),
            "request_id": request_id
        }


# --------------------------------------------------
# Question answering
# --------------------------------------------------

@app.post("/search")
def search_repository(
    request: QuestionRequest
):

    if vector_store is None:

        request_id = f"REQ-{uuid.uuid4().hex[:8]}"

        logger.warning(
            "Request ID: %s | Search attempted before repository indexing",
            request_id
        )

        return {
            "error": "Please index a repository first",
            "request_id": request_id
        }

    request_id = f"REQ-{uuid.uuid4().hex[:8]}"

    logger.info(
        "Request ID: %s | Query received: %s",
        request_id,
        request.question
    )

    previous_context = get_context()

    try:

        result = orchestrator.answer_question(
            vector_store,
            request.question,
            previous_context,
            request_id
        )

        add_message(
            "user",
            request.question
        )

        add_message(
            "assistant",
            result["answer"]
        )

        return {
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"],
            "request_id": request_id
        }

    except Exception as e:

        logger.error(
            "Request ID: %s | Answer generation failed: %s",
            request_id,
            str(e)
        )

        return {
            "error": str(e),
            "request_id": request_id
        }