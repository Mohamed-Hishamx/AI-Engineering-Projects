from agents.llm_client import call_llm

SYSTEM_PROMPT = """You triage a customer support message by severity. Reply
with exactly one word: high, medium, or low."""


def triage_ticket(state: dict) -> dict:
    severity = call_llm(SYSTEM_PROMPT, state["input_text"]).strip().lower()
    if severity not in ("high", "medium", "low"):
        severity = "low"

    state["ticket_severity"] = severity
    state["ticket_decision"] = {
        "high": "escalate_to_on_call_engineer",
        "medium": "assign_to_support_queue",
        "low": "auto_reply_with_kb_article",
    }[severity]

    state["final_output"] = (
        f"[SUPPORT] severity={severity} decision={state['ticket_decision']}"
    )
    return state
