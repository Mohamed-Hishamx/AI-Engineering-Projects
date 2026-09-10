"""
LangGraph StateGraph wiring together the router, lead qualification agent,
and support triage agent into one dynamic multi-agent workflow.
"""
from typing import TypedDict, Optional, Literal
from langgraph.graph import StateGraph, END

from agents.router import classify_intent
from agents.lead_qualifier import qualify_lead
from agents.support_triage import triage_ticket


class WorkflowState(TypedDict, total=False):
    input_text: str
    intent: Literal["lead", "support", "unknown"]
    lead_score: Optional[int]
    lead_decision: Optional[str]
    ticket_severity: Optional[str]
    ticket_decision: Optional[str]
    final_output: Optional[str]


def route_after_classification(state: WorkflowState) -> str:
    """Dynamic routing: picks the next node based on the router's output."""
    return {
        "lead": "qualify_lead",
        "support": "triage_support",
    }.get(state["intent"], "fallback")


def fallback_node(state: WorkflowState) -> WorkflowState:
    state["final_output"] = "Could not classify input; routed to human review."
    return state


def build_graph():
    graph = StateGraph(WorkflowState)

    graph.add_node("classify_intent", classify_intent)
    graph.add_node("qualify_lead", qualify_lead)
    graph.add_node("triage_support", triage_ticket)
    graph.add_node("fallback", fallback_node)

    graph.set_entry_point("classify_intent")

    graph.add_conditional_edges(
        "classify_intent",
        route_after_classification,
        {
            "qualify_lead": "qualify_lead",
            "triage_support": "triage_support",
            "fallback": "fallback",
        },
    )

    graph.add_edge("qualify_lead", END)
    graph.add_edge("triage_support", END)
    graph.add_edge("fallback", END)

    return graph.compile()
