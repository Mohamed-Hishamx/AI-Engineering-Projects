"""
Tests for ResearchAssistant.
OpenAI calls are mocked — no real API key needed to run tests.
"""

import json
import pytest
from unittest.mock import MagicMock, patch
from src.models import ResearchResponse
from src.assistant import ResearchAssistant

# ── Fixtures ──────────────────────────────────────────────────────────────────

VALID_RESPONSE = {
    "summary": "Photosynthesis is the process by which plants convert sunlight into glucose.",
    "key_points": [
        "Occurs in chloroplasts",
        "Requires sunlight, water, and CO2",
        "Produces glucose and oxygen",
    ],
    "follow_up_questions": [
        "What is the light-dependent reaction?",
        "How do C4 plants differ from C3 plants?",
        "What happens to glucose after photosynthesis?",
    ],
    "confidence": "high",
    "sources_note": "Biology textbooks, peer-reviewed plant science journals",
}


def make_mock_completion(content: dict):
    """Build a minimal mock that looks like an OpenAI ChatCompletion."""
    message = MagicMock()
    message.content = json.dumps(content)

    choice = MagicMock()
    choice.message = message

    usage = MagicMock()
    usage.total_tokens = 150

    completion = MagicMock()
    completion.choices = [choice]
    completion.usage = usage

    return completion


# ── Tests ─────────────────────────────────────────────────────────────────────

@patch("src.assistant.Groq")
def test_ask_returns_research_response(mock_groq_cls):
    """Happy path — valid JSON from Groq returns a ResearchResponse."""
    mock_client = MagicMock()
    mock_groq_cls.return_value = mock_client
    mock_client.chat.completions.create.return_value = make_mock_completion(VALID_RESPONSE)

    assistant = ResearchAssistant()
    result = assistant.ask("How does photosynthesis work?")

    assert isinstance(result, ResearchResponse)
    assert result.confidence == "high"
    assert len(result.key_points) == 3
    assert len(result.follow_up_questions) == 3


@patch("src.assistant.Groq")
def test_ask_passes_question_to_api(mock_groq_cls):
    """The user's question should appear in the user message."""
    mock_client = MagicMock()
    mock_groq_cls.return_value = mock_client
    mock_client.chat.completions.create.return_value = make_mock_completion(VALID_RESPONSE)

    assistant = ResearchAssistant()
    question = "What is quantum entanglement?"
    assistant.ask(question)

    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    messages = call_kwargs["messages"]
    user_message = next(m for m in messages if m["role"] == "user")
    assert user_message["content"] == question


@patch("src.assistant.Groq")
def test_ask_uses_json_mode(mock_groq_cls):
    """response_format must be json_object — this is what enforces structured output."""
    mock_client = MagicMock()
    mock_groq_cls.return_value = mock_client
    mock_client.chat.completions.create.return_value = make_mock_completion(VALID_RESPONSE)

    assistant = ResearchAssistant()
    assistant.ask("Test question")

    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["response_format"] == {"type": "json_object"}


@patch("src.assistant.Groq")
def test_ask_raises_on_invalid_schema(mock_groq_cls):
    """If Groq returns JSON that doesn't match our schema, Pydantic should raise."""
    from pydantic import ValidationError

    bad_response = {"summary": "Only a summary, missing all other fields"}

    mock_client = MagicMock()
    mock_groq_cls.return_value = mock_client
    mock_client.chat.completions.create.return_value = make_mock_completion(bad_response)

    assistant = ResearchAssistant()
    with pytest.raises(ValidationError):
        assistant.ask("Incomplete response test")


def test_research_response_model_validates_confidence():
    """confidence must be one of: high | medium | low."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        ResearchResponse(
            summary="Test",
            key_points=["Point"],
            follow_up_questions=["Question?"],
            confidence="very_high",  # not a valid literal
            sources_note="Some sources",
        )


def test_research_response_model_valid():
    """A correctly-formed dict should parse without errors."""
    result = ResearchResponse(**VALID_RESPONSE)
    assert result.summary == VALID_RESPONSE["summary"]
    assert result.confidence == "high"
