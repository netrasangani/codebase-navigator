import logging
import os
import shutil

from git import Repo


logger = logging.getLogger(__name__)


def clone_repository(
    repo_url,
    repo_path="../temp_repo",
    request_id=None
):
    """
    Clone a GitHub repository and return its local path.
    """

    logger.info(
        "Request ID: %s | Repository cloning started: %s",
        request_id,
        repo_url
    )

    # Remove previous repository if it exists
    if os.path.exists(repo_path):

        logger.info(
            "Request ID: %s | Removing previous repository: %s",
            request_id,
            repo_path
        )

        shutil.rmtree(repo_path)

    try:

        Repo.clone_from(
            repo_url,
            repo_path
        )

        logger.info(
            "Request ID: %s | Repository cloned successfully: %s",
            request_id,
            repo_path
        )

        return repo_path

    except Exception as e:

        logger.error(
            "Request ID: %s | Repository cloning failed: %s",
            request_id,
            str(e)
        )

        raise