"""
Application settings, loaded from environment variables / .env file.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Groq
    groq_api_key: str = Field(..., alias="GROQ_API_KEY")
    groq_model: str = Field(default="groq/compound", alias="GROQ_MODEL")

    # Database
    database_url: str = Field(..., alias="DATABASE_URL")

    # Embeddings
    embedding_model: str = Field(default="all-MiniLM-L6-v2", alias="EMBEDDING_MODEL")
    embedding_dimensions: int = Field(default=384, alias="EMBEDDING_DIMENSIONS")

    # Chunking
    chunk_size: int = Field(default=500, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=50, alias="CHUNK_OVERLAP")

    # Retrieval
    top_k_chunks: int = Field(default=5, alias="TOP_K_CHUNKS")

    # Langfuse
    langfuse_public_key: str = Field(default="", alias="LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key: str = Field(default="", alias="LANGFUSE_SECRET_KEY")
    
    

    # Auth (Clerk)
    clerk_jwks_url: str = Field(..., alias="CLERK_JWKS_URL")
    clerk_issuer: str = Field(..., alias="CLERK_ISSUER")

    # CORS: comma-separated list of allowed frontend origins
    allowed_origins: str = Field(..., alias="ALLOWED_ORIGINS")

    # Sentry
    sentry_dsn: str = Field(default="", alias="SENTRY_DSN")

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    model_config = {"env_file": ".env", "populate_by_name": True}


# Fails loudly at import time if any required setting is missing.
# Tests must set the required env vars explicitly (see tests/conftest.py).
settings = Settings()
