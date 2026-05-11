# Lead Qualification Agent

An AI agent that automatically researches and scores sales leads 1-10 using web search and LLMs.

## How it works

1. Send a lead (name + company) via POST request
2. Agent searches the web for company info using Tavily
3. Groq LLM reasons about the lead and scores them 1-10
4. Score + reasoning printed to console

## Tech Stack

- **FastAPI** — webhook endpoint
- **LangChain** — agent orchestration
- **Tavily** — web search for agents
- **Groq** — free, fast LLM (Llama 3.3)

## Setup

1. Clone the repo
2. Create a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate
```
3. Install dependencies:
```bash
   pip install fastapi uvicorn langchain langchain-groq langchain-tavily python-dotenv
```
4. Copy `.env.example` to `.env` and add your keys:
TAVILY_API_KEY=your-key  # tavily.com
GROQ_API_KEY=your-key    # console.groq.com
5. Run:
```bash
   uvicorn main:app --reload
```

## Test it

```bash
curl -X POST http://localhost:8000/qualify \
  -H "Content-Type: application/json" \
  -d '{"name": "Elon Musk", "company": "Tesla"}'
```

## Scoring

| Score | Meaning |
|-------|---------|
| 1-3 | Poor fit |
| 4-6 | Medium fit |
| 7-10 | Strong fit |