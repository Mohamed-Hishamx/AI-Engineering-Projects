# 🧠 Research Assistant CLI

A command-line research assistant powered by OpenAI. Ask any question and get a structured response: summary, key points, and follow-up questions — every time, validated by Pydantic.

## What this project demonstrates

| Concept | Implementation |
|---|---|
| Structured LLM output | OpenAI JSON mode + Pydantic schema validation |
| Config management | `pydantic-settings` loading from `.env` |
| Logging | Rotating file handler + console handler via `logging.config` |
| Testing | `pytest` with mocked OpenAI calls — no real API key needed |
| Dev hygiene | `.env.example`, `.gitignore`, `requirements.txt` |

## Example output

```
🔍 Your question: How does the immune system recognize pathogens?

⏳ Researching...

━━━ Summary ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The immune system recognizes pathogens through pattern recognition receptors
(PRRs) that detect conserved molecular structures called PAMPs. Innate immune
cells respond first, followed by adaptive immunity which creates targeted
antibodies and memory cells.

━━━ Key Points ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Toll-like receptors (TLRs) detect bacterial and viral signatures
  2. Dendritic cells bridge innate and adaptive immunity
  3. MHC molecules present antigens to T-cells
  4. B-cells produce antibodies specific to the pathogen

━━━ Follow-up Questions ━━━━━━━━━━━━━━━━━━━
  → What is the difference between innate and adaptive immunity?
  → How do vaccines exploit immunological memory?
  → What happens when the immune system misidentifies self as foreign?

Confidence: HIGH  |  Sources: Immunology textbooks, PubMed reviews
```

## Project structure

```
research-assistant/
├── src/
│   ├── main.py        # CLI entry point and REPL loop
│   ├── assistant.py   # OpenAI API calls + response parsing
│   ├── models.py      # Pydantic schema for structured output
│   ├── config.py      # Settings from .env + logging setup
│   └── display.py     # Terminal formatting (ANSI colours)
├── tests/
│   ├── test_assistant.py   # Unit tests with mocked OpenAI
│   └── test_display.py     # Output formatting tests
├── logs/              # Auto-created; rotating log files land here
├── .env.example       # Template — copy to .env and add your key
├── .gitignore
├── pytest.ini
└── requirements.txt
```

## Setup

```bash
# 1. Clone and enter the project
git clone https://github.com/Mohamed-Hishamx/N8N-Portfolio-Projects
cd research-assistant

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 5. Run
python -m src.main
```

## Running tests

Tests are fully mocked — no API key required:

```bash
pytest
```

## Key learning points

**Why JSON mode?** Passing `response_format={"type": "json_object"}` to OpenAI guarantees the response is valid JSON. Combined with Pydantic's `model_validate_json()`, you get a runtime guarantee that the response matches your schema — or an explicit error if it doesn't.

**Why pydantic-settings?** It reads from `.env` automatically and raises a clear error at startup if a required variable (like `OPENAI_API_KEY`) is missing — not buried in a runtime exception later.

**Why mock the OpenAI client in tests?** Real API calls in tests are slow, cost money, and fail when the network is down. `unittest.mock.patch` replaces the `OpenAI` class with a fake that returns whatever you define — so you test *your* logic, not OpenAI's infrastructure.

## Next step → Project 2: Docs Q&A Backend

This project calls OpenAI directly. Project 2 builds a FastAPI backend with a RAG pipeline: upload PDFs, chunk + embed them into pgvector, and expose a `POST /ask` endpoint that retrieves relevant context before calling the LLM.
