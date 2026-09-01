"""
Safety — prompt injection filter and PII redaction.

Two jobs:
1. Block prompt injection attacks before they reach the LLM
2. Redact personally identifiable information (PII) from questions
"""

import re
import logging

logger = logging.getLogger(__name__)

# Patterns that indicate a prompt injection attempt
INJECTION_PATTERNS = [
    r"ignore (all )?(previous|prior|above) instructions",
    r"forget (all )?(previous|prior|above) instructions",
    r"you are now",
    r"act as (a |an )?",
    r"pretend (you are|to be)",
    r"your (new )?instructions are",
    r"disregard (all )?(previous|prior)?",
    r"bypass (your )?(restrictions|guidelines|rules)",
    r"jailbreak",
    r"do anything now",
    r"dan mode",
]

# PII patterns to redact
PII_PATTERNS = [
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]"),
    (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[PHONE]"),
    (r"\b\+?[0-9]{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b", "[PHONE]"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "[SSN]"),
    (r"\b(?:\d{4}[-\s]?){3}\d{4}\b", "[CARD]"),
]


def check_prompt_injection(text: str) -> tuple[bool, str]:
    """
    Check if the text contains prompt injection patterns.
    Returns (is_safe, reason).
    """
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            logger.warning("Prompt injection detected: pattern '%s' in: %s", pattern, text[:100])
            return False, f"Request blocked: potential prompt injection detected."

    return True, ""


def redact_pii(text: str) -> str:
    """
    Replace PII patterns in text with safe placeholders.
    Applied to questions before they are logged or sent to the LLM.
    """
    redacted = text
    for pattern, replacement in PII_PATTERNS:
        redacted = re.sub(pattern, replacement, redacted)

    if redacted != text:
        logger.info("PII redacted from input")

    return redacted


def sanitize_input(text: str) -> tuple[bool, str, str]:
    """
    Full input sanitization pipeline:
    1. Check for prompt injection — block if found
    2. Redact PII from the text

    Returns (is_safe, sanitized_text, error_message)
    """
    is_safe, reason = check_prompt_injection(text)
    if not is_safe:
        return False, text, reason

    sanitized = redact_pii(text)
    return True, sanitized, ""