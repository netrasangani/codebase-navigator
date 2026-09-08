from langchain_core.tools import tool

from rag import search_code
from llm import llm
from context import add_message, get_context


vector_store = None


def set_vector_store(store):
    global vector_store

    # If a tuple is received, use only the FAISS vector store
    if isinstance(store, tuple):
        vector_store = store[0]
    else:
        vector_store = store


@tool
def search_codebase(query: str) -> str:
    """Search the indexed repository for relevant source code."""

    if vector_store is None:
        return "No repository has been indexed."

    results = search_code(
        vector_store,
        query
    )

    return "\n\n--- CODE CHUNK ---\n\n".join(
        results
    )


def ask_agent(question: str):

    previous_context = get_context()

    code_context = search_codebase.invoke(
        question
    )

    prompt = f"""
You are Codebase Navigator.

Previous conversation:
{previous_context}

Repository code:
{code_context}

Current question:
{question}

Answer using the repository code and previous conversation.
Do not invent files, classes, functions, or behavior.
Keep the answer concise.

Answer:
"""

    answer = llm.invoke(prompt)

    add_message(
        "user",
        question
    )

    add_message(
        "assistant",
        answer
    )

    return {
        "answer": answer,
        "source_code": code_context
    }