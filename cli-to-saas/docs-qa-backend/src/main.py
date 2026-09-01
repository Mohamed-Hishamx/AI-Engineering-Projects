"""
FastAPI application — Project 3 version.
Added: Sentry error tracking, Langfuse tracing, safety filtering, LLM evaluation.
"""

import logging
import sentry_sdk
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.database import get_db, init_db, Document, Chunk
from src.extraction import extract_text
from src.chunking import chunk_text
from src.embeddings import embed_batch
from src.rag_service import retrieve_relevant_chunks, build_context, generate_answer
from src.safety import sanitize_input
from src.observability import log_rag_query, flush
from src.evaluation import evaluate_answer
from src.config import settings

# Initialise Sentry — must happen before anything else
if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,  # trace 100% of requests
        environment="development",
    )

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title="Evaluated Support Bot", version="2.0.0")


@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("Database initialised.")


@app.on_event("shutdown")
def on_shutdown():
    flush()  # make sure all Langfuse events are sent before shutdown


class AskRequest(BaseModel):
    question: str
    user_id: str = "anonymous"


class AskResponse(BaseModel):
    answer: str
    sources: list[dict]
    evaluation: dict


class UploadResponse(BaseModel):
    document_id: int
    filename: str
    chunks_stored: int


@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a PDF or Markdown file."""
    file_bytes = await file.read()

    try:
        text = extract_text(file_bytes, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not text.strip():
        raise HTTPException(status_code=400, detail="No extractable text found in file.")

    chunks = chunk_text(text)
    if not chunks:
        raise HTTPException(status_code=400, detail="Document produced no usable chunks.")

    file_type = "pdf" if file.filename.lower().endswith(".pdf") else "markdown"
    document = Document(filename=file.filename, file_type=file_type)
    db.add(document)
    db.flush()

    vectors = embed_batch(chunks)
    for i, (chunk_content, vector) in enumerate(zip(chunks, vectors)):
        db.add(Chunk(
            document_id=document.id,
            content=chunk_content,
            chunk_index=i,
            embedding=vector,
        ))

    db.commit()
    logger.info("Stored '%s' with %d chunks", file.filename, len(chunks))

    return UploadResponse(
        document_id=document.id,
        filename=file.filename,
        chunks_stored=len(chunks),
    )


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, db: Session = Depends(get_db)):
    """
    Ask a question — with safety filtering, Langfuse tracing, and LLM evaluation.
    """
    # Step 1 — safety check
    is_safe, sanitized_question, error = sanitize_input(request.question)
    if not is_safe:
        raise HTTPException(status_code=400, detail=error)

    # Step 2 — placeholder for trace_id (assigned after generation)
    trace_id = None

    # Step 3 — retrieve relevant chunks
    chunks = retrieve_relevant_chunks(db, sanitized_question)
    if not chunks:
        return AskResponse(
            answer="No documents uploaded yet. Please upload a document first.",
            sources=[],
            evaluation={},
        )

    context = build_context(chunks)

    # Step 4 — generate answer
    answer = generate_answer(sanitized_question, context)

        # Step 5 — log the generation to Langfuse
    trace_id = log_rag_query(
        question=sanitized_question,
        context=context,
        answer=answer,
        user_id=request.user_id,
        model=settings.groq_model,
    )

    # Step 6 — evaluate the answer (LLM-as-judge)
    evaluation = evaluate_answer(
        question=sanitized_question,
        context=context,
        answer=answer,
        trace_id=trace_id,
    )

    return AskResponse(
        answer=answer,
        sources=[
            {
                "chunk_id": c.id,
                "document_id": c.document_id,
                "preview": c.content[:150],
            }
            for c in chunks
        ],
        evaluation=evaluation,
    )