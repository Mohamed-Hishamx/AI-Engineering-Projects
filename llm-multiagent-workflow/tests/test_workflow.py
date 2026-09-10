import os
import sys

os.environ.setdefault("USE_MOCK_LLM", "true")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from graph import build_graph


def test_lead_routing():
    app = build_graph()
    result = app.invoke({"input_text": "Enterprise team of 30, urgent, need a quote this week"})
    assert result["intent"] == "lead"
    assert result["lead_decision"] == "route_to_sales_rep"


def test_support_routing_high_severity():
    app = build_graph()
    result = app.invoke({"input_text": "The app is down for all users, critical outage"})
    assert result["intent"] == "support"
    assert result["ticket_severity"] == "high"
    assert result["ticket_decision"] == "escalate_to_on_call_engineer"


def test_unknown_routing_falls_back():
    app = build_graph()
    result = app.invoke({"input_text": "hello there"})
    assert result["intent"] == "unknown"
    assert "human review" in result["final_output"]


if __name__ == "__main__":
    test_lead_routing()
    test_support_routing_high_severity()
    test_unknown_routing_falls_back()
    print("All tests passed.")
