"""
Tests for display helpers.
Verifies output contains the right content without caring about ANSI codes.
"""

import pytest
from src.models import ResearchResponse
from src.display import print_result, print_banner

SAMPLE = ResearchResponse(
    summary="Black holes are regions where gravity is so strong that nothing can escape.",
    key_points=["Formed from collapsed massive stars", "Defined by an event horizon", "Emit Hawking radiation"],
    follow_up_questions=["What happens at the singularity?", "Can information escape a black hole?"],
    confidence="medium",
    sources_note="Astrophysics journals, NASA publications",
)


def strip_ansi(text: str) -> str:
    import re
    return re.sub(r"\033\[[0-9;]*m", "", text)


def test_print_result_contains_summary(capsys):
    print_result(SAMPLE)
    captured = strip_ansi(capsys.readouterr().out)
    assert "Black holes" in captured


def test_print_result_contains_key_points(capsys):
    print_result(SAMPLE)
    captured = strip_ansi(capsys.readouterr().out)
    assert "event horizon" in captured


def test_print_result_contains_confidence(capsys):
    print_result(SAMPLE)
    captured = strip_ansi(capsys.readouterr().out)
    assert "MEDIUM" in captured


def test_print_banner_runs(capsys):
    print_banner()
    captured = capsys.readouterr().out
    assert "Research Assistant" in captured
