from agents.llm_client import call_llm

SYSTEM_PROMPT = """You classify an inbound message as either a sales "lead" or a
"support" request. Reply with exactly one word: lead, support, or unknown."""


def classify_intent(state: dict) -> dict:
    intent = call_llm(SYSTEM_PROMPT, state["input_text"]).strip().lower()
    if intent not in ("lead", "support"):
        intent = "unknown"
    state["intent"] = intent
    return state
