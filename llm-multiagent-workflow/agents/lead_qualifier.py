from agents.llm_client import call_llm

SYSTEM_PROMPT = """You qualify a sales lead from their message. Reply with only
an integer 0-100 score representing purchase intent and fit."""


def qualify_lead(state: dict) -> dict:
    raw_score = call_llm(SYSTEM_PROMPT, state["input_text"]).strip()
    try:
        score = int("".join(c for c in raw_score if c.isdigit())[:3] or 0)
    except ValueError:
        score = 0

    state["lead_score"] = score
    if score >= 70:
        state["lead_decision"] = "route_to_sales_rep"
    elif score >= 40:
        state["lead_decision"] = "add_to_nurture_sequence"
    else:
        state["lead_decision"] = "auto_decline"

    state["final_output"] = (
        f"[LEAD] score={score} decision={state['lead_decision']}"
    )
    return state
