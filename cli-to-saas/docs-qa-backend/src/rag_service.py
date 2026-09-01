"""
RAG service — ties together retrieval (pgvector similarity search) and
generation (Groq) into the final answer pipeline.
"""

import logging
from groq import Groq
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database import Chunk
from src.embeddings import embed_text
from src.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a helpful assistant that answers questions using ONLY the provided
context. If the context doesn't contain enough information to answer the question, say so
clearly — do not make up information.

Always cite which part of the context supports your answer where possible."""


def retrieve_relevant_chunks(db: Session, question: str, top_k: int = None) -> list[Chunk]:
    """
    Embed the question and find the top_k most similar chunks in the database
    using cosine distance — smaller distance means more similar.
    """
    top_k = top_k or settings.top_k_chunks
    question_vector = embed_text(question)

    stmt = (
        select(Chunk)
        .order_by(Chunk.embedding.cosine_distance(question_vector))
        .limit(top_k)
    )
    results = db.execute(stmt).scalars().all()
    logger.info("Retrieved %d chunks for question: %s", len(results), question[:60])
    return results


def build_context(chunks: list[Chunk]) -> str:
    """Format retrieved chunks into a single context block for the prompt."""
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(f"[Source {i}]\n{chunk.content}")
    return "\n\n".join(parts)


def generate_answer(question: str, context: str) -> str:
    """Send the question + retrieved context to Groq and return the answer."""
    client = Groq(api_key=settings.groq_api_key)

    user_message = f"""Context:
{context}

Question: {question}

Answer the question using only the context above."""

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


def ask_question(db: Session, question: str) -> dict:
    """Full RAG pipeline: retrieve relevant chunks, build context, generate answer."""
    chunks = retrieve_relevant_chunks(db, question)

    if not chunks:
        return {
            "answer": "No documents have been uploaded yet. Please upload a document first.",
            "sources": [],
        }

    context = build_context(chunks)
    answer = generate_answer(question, context)

    return {
        "answer": answer,
        "sources": [
            {
                "chunk_id": c.id,
                "document_id": c.document_id,
                "preview": c.content[:150],
            }
            for c in chunks
        ],
    }