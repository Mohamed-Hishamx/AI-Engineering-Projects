"""
Embeddings — converts text into vectors using a local sentence-transformers model.

The model loads once at import time and is reused for every request.
"""

import logging
from sentence_transformers import SentenceTransformer
from src.config import settings

logger = logging.getLogger(__name__)

logger.info("Loading embedding model: %s", settings.embedding_model)
_model = SentenceTransformer(settings.embedding_model)
logger.info("Embedding model loaded.")


def embed_text(text: str) -> list[float]:
    """Embed a single piece of text — returns a vector as a list of floats."""
    vector = _model.encode(text, normalize_embeddings=True)
    return vector.tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed multiple texts at once — much faster than calling embed_text in a loop."""
    vectors = _model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return vectors.tolist()