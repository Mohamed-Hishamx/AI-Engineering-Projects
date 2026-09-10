"""
Thin LLM wrapper.

Defaults to USE_MOCK_LLM=true so the whole workflow runs deterministically
and for free, with no API key required. Set USE_MOCK_LLM=false and provide
OPENAI_API_KEY to run it against a real model via LangChain.
"""
import os

USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "true").lower() == "true"


def call_llm(system_prompt: str, user_prompt: str) -> str:
    if USE_MOCK_LLM:
        return _mock_response(system_prompt, user_prompt)

    from langchain_openai import ChatOpenAI
    from langchain_core.messages import SystemMessage, HumanMessage

    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
    result = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
    return result.content


def _mock_response(system_prompt: str, user_prompt: str) -> str:
    """Rule-based stand-in for an LLM call, used for free/offline runs and tests."""
    text = user_prompt.lower()

    if "classify" in system_prompt.lower():
        if any(k in text for k in ["price", "pricing", "demo", "buy", "quote", "interested in"]):
            return "lead"
        if any(k in text for k in ["broken", "error", "not working", "issue", "help", "bug", "down"]):
            return "support"
        return "unknown"

    if "qualify" in system_prompt.lower():
        score = 40
        if "budget" in text or "this week" in text or "urgent" in text:
            score += 30
        if "enterprise" in text or "team of" in text:
            score += 20
        score = min(score, 100)
        return str(score)

    if "severity" in system_prompt.lower():
        if any(k in text for k in ["down", "outage", "can't login", "critical", "all users"]):
            return "high"
        if any(k in text for k in ["slow", "bug", "minor"]):
            return "medium"
        return "low"

    return "unknown"
