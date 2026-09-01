"""
Text extraction — pulls raw text out of uploaded PDF or Markdown files.
"""

import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract all text from a PDF, page by page."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text_parts = []
    for page_num, page in enumerate(doc):
        text_parts.append(page.get_text())
    doc.close()
    full_text = "\n".join(text_parts)
    logger.info("Extracted %d characters from PDF (%d pages)", len(full_text), page_num + 1)
    return full_text


def extract_text_from_markdown(file_bytes: bytes) -> str:
    """Markdown is already plain text — just decode it."""
    text = file_bytes.decode("utf-8")
    logger.info("Extracted %d characters from Markdown", len(text))
    return text


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Dispatch to the right extractor based on file extension."""
    if filename.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith((".md", ".markdown", ".txt")):
        return extract_text_from_markdown(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {filename}. Use .pdf, .md, or .txt")