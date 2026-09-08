import logging
from contextvars import ContextVar

from langchain_core.tools import tool

from agents.repository_agent import clone_repository
from agents.code_analysis_agent import analyze_repository
from agents.retrieval_agent import retrieve_code


logger = logging.getLogger(__name__)


# Stores the Request ID for the current agentic execution
current_request_id = ContextVar(
    "current_request_id",
    default=None
)


# Shared vector store
vector_store = None


def set_request_id(request_id):
    current_request_id.set(request_id)


def set_vector_store(store):
    global vector_store
    vector_store = store


@tool
def repository_tool(repo_url: str) -> str:
    """
    Clone a GitHub repository.
    """

    request_id = current_request_id.get()

    logger.info(
        "Request ID: %s | Repository Tool invoked",
        request_id
    )

    repo_path = clone_repository(
        repo_url,
        request_id=request_id
    )

    return repo_path


@tool
def code_analysis_tool(repo_path: str) -> str:
    """
    Analyze repository code and create the FAISS vector store.
    """

    global vector_store

    request_id = current_request_id.get()

    logger.info(
        "Request ID: %s | Code Analysis Tool invoked",
        request_id
    )

    vector_store, files, chunks = analyze_repository(
        repo_path,
        request_id=request_id
    )

    return (
        f"Repository analyzed successfully. "
        f"Files: {files}. "
        f"Chunks: {chunks}."
    )


@tool
def retrieval_tool(query: str) -> str:
    """
    Retrieve relevant code from the indexed repository.
    """

    request_id = current_request_id.get()

    logger.info(
        "Request ID: %s | Retrieval Tool invoked",
        request_id
    )

    if vector_store is None:

        logger.warning(
            "Request ID: %s | No repository has been indexed",
            request_id
        )

        return "No repository has been indexed."

    results = retrieve_code(
        vector_store,
        query,
        request_id=request_id
    )

    if not results:

        return "No relevant repository code was found."

    output = []

    for result in results:

        output.append(
            f"""
FILE: {result['file']}

{result['code']}
"""
        )

    return "\n---\n".join(output)