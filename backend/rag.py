import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


def load_code(repo_path):
    documents = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            d for d in dirs
            if d != ".git"
        ]

        for file in files:

            if file.endswith(
                (
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
            ):

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

                except Exception:
                    continue

    return documents


def create_vector_store(repo_path):

    documents = load_code(repo_path)

    if not documents:
        raise ValueError(
            "No supported source files found in repository."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(
        documents
    )

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vector_store, len(documents), len(chunks)


def search_code(vector_store, query):

    results = vector_store.similarity_search(
        query,
        k=3
    )

    formatted_results = []

    for doc in results:

        file_path = doc.metadata.get(
            "source",
            "Unknown file"
        )

        formatted_results.append(
            f"FILE: {file_path}\n\n{doc.page_content}"
        )

    return formatted_results