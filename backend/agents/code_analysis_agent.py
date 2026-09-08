import logging
import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


logger = logging.getLogger(__name__)


embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


def analyze_repository(
    repo_path,
    request_id=None
):
    """
    Read supported source files, split them into chunks,
    create embeddings, and build a FAISS vector store.
    """

    logger.info(
        "Request ID: %s | Code analysis started: %s",
        request_id,
        repo_path
    )

    documents = []

    supported_extensions = (
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".java",
        ".cpp",
        ".c",
        ".h",
        ".md"
    )

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            d for d in dirs
            if d != ".git"
        ]

        for file in files:

            if not file.endswith(
                supported_extensions
            ):
                continue

            path = os.path.join(
                root,
                file
            )

            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:

                    content = f.read()

                documents.append(
                    Document(
                        page_content=content,
                        metadata={
                            "source": path
                        }
                    )
                )

            except Exception as e:

                logger.warning(
                    "Request ID: %s | Could not read file %s: %s",
                    request_id,
                    path,
                    str(e)
                )

                continue

    if not documents:

        logger.error(
            "Request ID: %s | No supported source files found",
            request_id
        )

        raise ValueError(
            "No supported source files found in repository."
        )

    logger.info(
        "Request ID: %s | Source files loaded: %s",
        request_id,
        len(documents)
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(
        documents
    )

    logger.info(
        "Request ID: %s | Code chunks created: %s",
        request_id,
        len(chunks)
    )

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    logger.info(
        "Request ID: %s | Embeddings generated and FAISS vector store created",
        request_id
    )

    return (
        vector_store,
        len(documents),
        len(chunks)
    )