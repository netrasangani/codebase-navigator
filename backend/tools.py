from langchain_core.tools import tool
from rag import search_code


@tool
def search_codebase(query: str) -> str:
    """Search the indexed codebase for relevant code."""
    
    from main import vector_store

    if vector_store is None:
        return "No repository has been indexed yet."

    results = search_code(vector_store, query)

    return "\n\n".join(results)