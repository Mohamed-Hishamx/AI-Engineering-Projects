# Docs Q&A Backend

FastAPI service for question answering over your own documents (PDF or Markdown).

## How it works

1. `POST /upload` extracts text, splits it into chunks, embeds them (sentence-transformers `all-MiniLM-L6-v2`) and stores them in Postgres with pgvector.
2. `POST /ask` checks the question for prompt injection and PII, retrieves the closest chunks, and asks a Groq model to answer using only that context.
3. The answer is logged to Langfuse and scored by an LLM judge. The response includes sources and the evaluation.

Both endpoints require a Clerk session token. The user ID comes from the verified token, and documents and chunks are stored with that user ID. Retrieval only searches the caller's own chunks.

## Endpoints

| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | `/health` | none | Process is up. Does not check the database or model |
| POST | `/upload` | Bearer token | Upload a PDF or Markdown file |
| POST | `/ask` | Bearer token | Body: `{"question": "..."}` |

## Setup

Requirements: Python 3.11+, Postgres with the pgvector extension, a Groq API key, a Clerk application.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env     # then fill in the values
uvicorn src.main:app --reload
```

## Environment variables

| Variable | Required | Notes |
|---|---|---|
| `GROQ_API_KEY` | yes | |
| `DATABASE_URL` | yes | Postgres connection string |
| `CLERK_JWKS_URL` | yes | `https://<your-clerk-domain>/.well-known/jwks.json` |
| `CLERK_ISSUER` | yes | `https://<your-clerk-domain>` |
| `ALLOWED_ORIGINS` | yes | Comma-separated frontend origins, for example `http://localhost:3000` |
| `GROQ_MODEL`, `EMBEDDING_MODEL`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `TOP_K_CHUNKS` | no | Have defaults, see `src/config.py` |
| `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `SENTRY_DSN` | no | Observability |

The app refuses to start if a required variable is missing.

## Database

Tables are created on startup with `create_all`. There are no migrations yet. If you already had `documents` and `chunks` tables from an older version, add the new column manually:

```sql
ALTER TABLE documents ADD COLUMN user_id TEXT NOT NULL DEFAULT 'legacy';
ALTER TABLE chunks ADD COLUMN user_id TEXT NOT NULL DEFAULT 'legacy';
```

## Deploy

`railway.toml` and `Procfile` are set up for Railway. Set the environment variables above in the Railway service.

## Tests

```bash
pytest
```

`tests/conftest.py` sets dummy values for the required variables. There is no API regression suite yet, including no cross-user access test.

## Known limits

- No file size limit on upload yet.
- Safety checks are English regex patterns only.
- No migrations, no published evaluation results.
- Answer citations are the retrieved chunks. They are not checked to support each claim.
