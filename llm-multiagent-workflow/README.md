# LLM Multi-Agent Workflow Automation

A small multi-agent system built with **Python, LangChain, and LangGraph** that
automates lead qualification, customer support triage, and dynamic workflow
execution.

## Architecture

```
                 ┌───────────────────┐
 input_text ---> │  classify_intent   │  (router agent)
                 └─────────┬─────────┘
                            │  dynamic routing based on intent
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
      qualify_lead   triage_support    fallback
      (lead agent)   (support agent)  (human review)
```

- **Router agent** (`agents/router.py`) classifies an inbound message as a
  sales lead, a support request, or unknown, and LangGraph dynamically
  branches to the right agent.
- **Lead qualification agent** (`agents/lead_qualifier.py`) scores intent/fit
  and decides: route to sales rep, add to nurture sequence, or auto-decline.
- **Support triage agent** (`agents/support_triage.py`) scores severity and
  decides: escalate to on-call, assign to queue, or auto-reply with a KB
  article.
- **`graph.py`** wires all three into one `StateGraph` with conditional edges,
  so the workflow executed depends on what comes in.

## Running it for free

By default `USE_MOCK_LLM=true`, so the agents use a deterministic rule-based
stand-in instead of calling any paid API. This is enough to demonstrate the
full graph, routing, and decision logic with zero token cost.

```bash
pip install -r requirements.txt
python main.py
```

## Running it against a real model

```bash
export USE_MOCK_LLM=false
export OPENAI_API_KEY=sk-...
python main.py "We're an enterprise team of 40, need pricing this week"
```

## Tests

```bash
python tests/test_workflow.py
```
