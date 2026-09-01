"""
Database layer — SQLAlchemy models + pgvector column type.

Two tables:
  documents — one row per uploaded file
  chunks    — one row per text chunk, with its embedding vector
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from pgvector.sqlalchemy import Vector
from src.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    uploaded_at = Column(DateTime, server_default=func.now())

    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    embedding = Column(Vector(settings.embedding_dimensions), nullable=False)

    document = relationship("Document", back_populates="chunks")


def init_db():
    """Create tables and enable the pgvector extension if not already enabled."""
    with engine.connect() as conn:
        conn.execute(__import__("sqlalchemy").text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency — yields a session, closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()