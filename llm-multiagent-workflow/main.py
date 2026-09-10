"""
Demo entry point.

Run:
    python main.py "We're a 40-person team, urgent, need pricing for the enterprise plan"
    python main.py "Production is down, all users are seeing errors"

Runs fully offline/free by default (USE_MOCK_LLM=true). To use a real model:
    export USE_MOCK_LLM=false
    export OPENAI_API_KEY=sk-...
    python main.py "..."
"""
import sys
from graph import build_graph

SAMPLE_INPUTS = [
    "Hi, we're an enterprise team of 50 and want a demo + pricing this week, budget approved.",
    "Just browsing, no rush, might look into this later.",
    "Production is down for all users, this is critical, please help now.",
    "Small bug: the export button is a bit slow sometimes.",
]


def run(text: str):
    app = build_graph()
    result = app.invoke({"input_text": text})
    print(f"input:  {text}")
    print(f"intent: {result.get('intent')}")
    print(f"output: {result.get('final_output')}")
    print("-" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(" ".join(sys.argv[1:]))
    else:
        for sample in SAMPLE_INPUTS:
            run(sample)
