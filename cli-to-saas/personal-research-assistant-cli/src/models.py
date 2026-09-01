"""
Data models — define the shape of the LLM response.
Pydantic validates the JSON from OpenAI against this schema at runtime.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ResearchResponse(BaseModel):
    summary: str = Field(..., description="Concise 2-4 sentence answer")
    key_points: list[str] = Field(..., min_length=1, max_length=5)
    follow_up_questions: list[str] = Field(..., min_length=1, max_length=5)
    confidence: Literal["high", "medium", "low"]
    sources_note: str = Field(..., description="What sources would verify this")
