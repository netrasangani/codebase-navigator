import logging

from agents.repository_agent import clone_repository
from agents.code_analysis_agent import analyze_repository
from agents.answer_agent import generate_answer

from agents.tools import (
    repository_tool,
    code_analysis_tool,
    retrieval_tool,
    set_vector_store,
    set_request_id
)


logger = logging.getLogger(__name__)


class CodebaseOrchestrator:

    def __init__(self):

        self.code_context = ""

        self.tools = {
            "REPOSITORY": repository_tool,
            "CODE_ANALYSIS": code_analysis_tool,
            "RETRIEVE": retrieval_tool
        }

    # ==================================================
    # REPOSITORY INDEXING
    # ==================================================

    def index_repository(
        self,
        repo_url,
        request_id=None
    ):

        # Store Request ID for the complete workflow
        set_request_id(request_id)

        logger.info(
            "Request ID: %s | Orchestrator started repository workflow",
            request_id
        )

        # ----------------------------------------------
        # Repository Tool
        # ----------------------------------------------

        logger.info(
            "Request ID: %s | Orchestrator selected Repository Tool",
            request_id
        )

        repo_path = clone_repository(
            repo_url,
            request_id=request_id
        )

        # ----------------------------------------------
        # Code Analysis Tool
        # ----------------------------------------------

        logger.info(
            "Request ID: %s | Orchestrator selected Code Analysis Tool",
            request_id
        )

        vector_store, files, chunks = analyze_repository(
            repo_path,
            request_id=request_id
        )

        # Make vector store available to Retrieval Tool
        set_vector_store(vector_store)

        logger.info(
            "Request ID: %s | Orchestrator completed repository workflow",
            request_id
        )

        return {
            "vector_store": vector_store,
            "files": files,
            "chunks": chunks
        }

    # ==================================================
    # ORCHESTRATOR DECISION
    # ==================================================

    def decide_action(
        self,
        question,
        previous_context="",
        request_id=None
    ):

        logger.info(
            "Request ID: %s | Orchestrator deciding next action",
            request_id
        )

        # ----------------------------------------------
        # No evidence → Retrieval is required
        # ----------------------------------------------

        if not self.code_context:

            logger.info(
                "Request ID: %s | No repository evidence | Decision: RETRIEVE",
                request_id
            )

            return "RETRIEVE"

        # ----------------------------------------------
        # Evidence available → Generate answer
        # ----------------------------------------------

        logger.info(
            "Request ID: %s | Repository evidence available | Decision: ANSWER",
            request_id
        )

        return "ANSWER"

    # ==================================================
    # AGENTIC QUESTION WORKFLOW
    # ==================================================

    def answer_question(
        self,
        vector_store,
        question,
        previous_context="",
        request_id=None
    ):

        # Set the Request ID for all tools
        set_request_id(request_id)

        logger.info(
            "Request ID: %s | Orchestrator started agentic workflow",
            request_id
        )

        # Reset previous evidence
        self.code_context = ""

        # Make current vector store available
        # to the Retrieval Tool
        set_vector_store(vector_store)

        # ==================================================
        # STEP 1 — ORCHESTRATOR DECISION
        # ==================================================

        action = self.decide_action(
            question,
            previous_context,
            request_id
        )

        # ==================================================
        # STEP 2 — RETRIEVAL TOOL
        # ==================================================

        if action == "RETRIEVE":

            logger.info(
                "Request ID: %s | Orchestrator invoking Retrieval Tool",
                request_id
            )

            self.code_context = retrieval_tool.invoke({
                "query": question
            })

            logger.info(
                "Request ID: %s | Retrieval Tool observation received",
                request_id
            )

        # ==================================================
        # STEP 3 — ORCHESTRATOR DECIDES AGAIN
        # ==================================================

        action = self.decide_action(
            question,
            previous_context,
            request_id
        )

        # ==================================================
        # STEP 4 — ANSWER AGENT
        # ==================================================

        if action == "ANSWER":

            logger.info(
                "Request ID: %s | Orchestrator selected Answer Agent",
                request_id
            )

            answer = generate_answer(
                question,
                self.code_context,
                previous_context,
                request_id=request_id
            )

            logger.info(
                "Request ID: %s | Orchestrator completed agentic workflow",
                request_id
            )

            return {
                "answer": answer,
                "sources": self.code_context
            }

        # ==================================================
        # FALLBACK
        # ==================================================

        return {
            "answer": "The orchestrator could not determine the next action.",
            "sources": self.code_context
        }