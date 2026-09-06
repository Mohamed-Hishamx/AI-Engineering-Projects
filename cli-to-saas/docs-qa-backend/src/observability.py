"""
Observability — Langfuse tracing for every LLM call.
Built for Langfuse v3 API.
"""

from langfuse import Langfuse
from langfuse.types import TraceContext
from src.config import settings

langfuse = Langfuse(
    public_key=settings.langfuse_public_key,
    secret_key=settings.langfuse_secret_key,
)


def log_rag_query(question: str, context: str, answer: str, user_id: str, model: str) -> str:
    trace_id = langfuse.create_trace_id()
    langfuse.create_event(
        trace_id=trace_id,
        name="rag_answer",
        input=f"Question: {question}\n\nContext: {context}",
        output=answer,
        metadata={"model": model, "user_id": user_id},
    )
    return trace_id


def log_score(trace_id: str, name: str, value: float, comment: str = None):
    """Attach a score to a trace."""
    langfuse.create_score(
        trace_id=trace_id,
        name=name,
        value=value,
        comment=comment,
    )


def flush():
    """Force-send any buffered events to Langfuse."""
    langfuse.flush()