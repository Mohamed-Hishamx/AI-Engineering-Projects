"""
ResearchAssistant — wraps Groq chat completions and enforces structured output
via Pydantic model + JSON mode.
"""

import logging
from groq import Groq
from src.models import ResearchResponse
from src.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert research assistant. When given a question, respond ONLY with a
valid JSON object matching this exact schema:

{
  "summary": "A clear, concise 2-4 sentence answer to the question",
  "key_points": ["Point 1", "Point 2", "Point 3"],
  "follow_up_questions": ["Follow-up 1?", "Follow-up 2?", "Follow-up 3?"],
  "confidence": "high | medium | low",
  "sources_note": "A brief note on what kinds of sources would verify this"
}

Rules:
- key_points: 3-5 bullet points, each one factual and self-contained
- follow_up_questions: 3 questions that would deepen understanding of the topic
- confidence: reflect how well-established the answer is
- Do NOT include markdown, code blocks, or any text outside the JSON object
"""


class ResearchAssistant:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.model
        logger.info("ResearchAssistant initialised with model=%s", self.model)

    def ask(self, question: str) -> ResearchResponse:
        """Send a question to the LLM and return a validated ResearchResponse."""
        logger.info("Sending question: %s", question[:80])

        response = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
        )

        raw = response.choices[0].message.content
        logger.debug("Raw response: %s", raw)

        result = ResearchResponse.model_validate_json(raw)

        logger.info(
            "Response received — confidence=%s, tokens_used=%d",
            result.confidence,
            response.usage.total_tokens,
        )

        return result