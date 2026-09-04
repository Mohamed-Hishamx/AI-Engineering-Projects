"""
Evaluation — LLM-as-judge scoring system.
"""

import json
import logging
from groq import Groq
from src.config import settings
from src.observability import log_score

logger = logging.getLogger(__name__)

JUDGE_PROMPT = """You are an expert evaluator for a RAG system.

You will be given a question, retrieved context, and an AI-generated answer.

Score the answer on two dimensions from 1 to 5:

FAITHFULNESS (1-5): Is the answer grounded in the provided context?
- 5: Every claim is directly supported by the context
- 3: Most claims are supported, minor additions from outside
- 1: Answer contains significant hallucination

RELEVANCE (1-5): Does the answer actually address the question?
- 5: Directly and completely addresses the question
- 3: Partially addresses the question
- 1: Does not address the question at all

You MUST respond with ONLY a raw JSON object. No markdown, no backticks, no explanation. Start your response with { and end with }.
Example: {"faithfulness": 5, "relevance": 4, "reasoning": "The answer is grounded in the context."}"""


def evaluate_answer(
    question: str,
    context: str,
    answer: str,
    trace_id: str,
) -> dict:
    """Score an answer using LLM-as-judge and attach scores to Langfuse trace."""
    client = Groq(api_key=settings.groq_api_key)

    user_message = f"""Question: {question}

Context:
{context}

Answer:
{answer}"""

    try:
        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {"role": "system", "content": JUDGE_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.1,
        )

        raw = response.choices[0].message.content
        scores = json.loads(raw)

        faithfulness = float(scores.get("faithfulness", 0))
        relevance = float(scores.get("relevance", 0))
        reasoning = scores.get("reasoning", "")

        log_score(trace_id, "faithfulness", faithfulness, reasoning)
        log_score(trace_id, "relevance", relevance, reasoning)

        logger.info(
            "Evaluation — faithfulness=%.1f, relevance=%.1f",
            faithfulness,
            relevance,
        )

        return {
            "faithfulness": faithfulness,
            "relevance": relevance,
            "reasoning": reasoning,
        }

    except Exception as e:
        logger.error("Evaluation failed: %s", e)
        return {"faithfulness": -1, "relevance": -1, "reasoning": "Evaluation skipped — rate limit or model unavailable"}