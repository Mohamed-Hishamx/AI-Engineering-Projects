"""
Chunking — splits long text into overlapping pieces sized for embedding.
"""

import logging
from src.config import settings

logger = logging.getLogger(__name__)


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> list[str]:
    """
    Split text into chunks of roughly `chunk_size` characters, with `overlap`
    characters shared between consecutive chunks.
    """
    chunk_size = chunk_size or settings.chunk_size
    overlap = overlap or settings.chunk_overlap

    if len(text) <= chunk_size:
        return [text.strip()] if text.strip() else []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        if end < len(text):
            last_space = text.rfind(" ", start, end)
            if last_space > start:
                end = last_space

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap
        if start <= 0 or end >= len(text):
            break

    logger.info(
        "Split text into %d chunks (size=%d, overlap=%d)",
        len(chunks), chunk_size, overlap
    )
    return chunks