"""
Observability — Langfuse tracing for every LLM call.
Built for Langfuse v3 API.
"""

from langfuse import Langfuse
from src.config import settings

langfuse = Langfuse(
    public_key=settings.langfuse_public_key,
    secret_key=settings.langfuse_secret_key,
)


def log_rag_query(question: str, context: str, answer: str, user_id: str = "anonymous", model: str = None) -> str:
    trace_id = langfuse.create_trace_id()
    langfuse.create_event(
        name="rag-query",
        input={"question": question, "context": context},
        output=answer,
        metadata={"user_id": user_id, "model": model, "trace_id": trace_id},
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