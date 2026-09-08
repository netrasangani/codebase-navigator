import logging
import os


logger = logging.getLogger(__name__)


def retrieve_code(
    vector_store,
    query,
    k=5,
    request_id=None
):
    """
    Retrieval Agent.

    Searches the FAISS vector store and returns
    the most relevant repository code chunks.
    """

    logger.info(
        "Request ID: %s | Retrieval Agent started | Query: %s",
        request_id,
        query
    )

    if vector_store is None:

        logger.warning(
            "Request ID: %s | Retrieval Agent: no vector store available",
            request_id
        )

        return []

    try:

        results = vector_store.similarity_search_with_score(
            query,
            k=k
        )

        logger.info(
            "Request ID: %s | FAISS search completed | Results: %s",
            request_id,
            len(results)
        )

    except Exception as e:

        logger.error(
            "Request ID: %s | Retrieval Agent failed: %s",
            request_id,
            str(e)
        )

        raise

    formatted_results = []

    for doc, score in results:

        file_path = doc.metadata.get(
            "source",
            "Unknown file"
        )

        file_name = os.path.basename(file_path)

        # Ignore documentation/history files
        if file_name in {
            "HISTORY.md",
            "CHANGELOG.md",
            "LICENSE"
        }:

            logger.info(
                "Request ID: %s | Retrieval Agent ignored file: %s",
                request_id,
                file_name
            )

            continue

        formatted_results.append(
            {
                "file": file_path,
                "code": doc.page_content,
                "score": float(score)
            }
        )

    logger.info(
        "Request ID: %s | Retrieval Agent completed | Relevant chunks: %s",
        request_id,
        len(formatted_results)
    )

    return formatted_results