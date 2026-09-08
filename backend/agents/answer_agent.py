import logging

from llm import llm


logger = logging.getLogger(__name__)


def generate_answer(
    question,
    code_context,
    previous_context="",
    request_id=None
):
    """
    Answer Agent.

    Generates a grounded answer using the retrieved
    repository evidence.
    """

    logger.info(
        "Request ID: %s | Answer Agent started | Query: %s",
        request_id,
        question
    )

    prompt = f"""
You are Codebase Navigator, an AI assistant that explains
software repositories.

Answer the user's question using ONLY the repository evidence
provided below.

Previous conversation:
{previous_context}

Repository evidence:
{code_context}

Current question:
{question}

IMPORTANT RULES:

1. Treat each FILE section as a separate source file.

2. A class written like:
   class Child(Base):
   means Child INHERITS FROM Base.
   It does NOT mean Child is inside Base.

3. A function written outside a class is NOT a method of that class.

4. Do not move functions, variables, or classes from one part of
   the code into another class.

5. Identify the exact class or function shown in the evidence
   before explaining its purpose.

6. If the evidence contains multiple authentication classes,
   distinguish their roles instead of combining them.

7. Mention the actual filename when useful.

8. Do not invent files, classes, functions, variables, or behavior.

9. Do not use general programming knowledge to fill missing
   repository information.

10. If the evidence is insufficient, say:
   "I couldn't find enough information in the retrieved
   repository code to answer this confidently."

11. Keep the answer concise and factual.

12. Prefer a direct answer in 2-4 sentences.

Answer:
"""

    try:

        answer = llm.invoke(prompt)

        logger.info(
            "Request ID: %s | Answer Agent completed",
            request_id
        )

        return answer

    except Exception as e:

        logger.error(
            "Request ID: %s | Answer Agent failed: %s",
            request_id,
            str(e)
        )

        raise