# AI Engineering Projects

Portfolio of applied AI projects by Mohamed Hisham. Each folder has its own README with setup steps and limits.

## Projects

| Folder | What it is | Status |
|---|---|---|
| `cli-to-saas/personal-research-assistant-cli` | CLI research assistant using Groq with Pydantic-validated structured output and mocked tests | Learning project |
| `cli-to-saas/docs-qa-backend` | FastAPI RAG backend: upload PDF/Markdown, chunk, embed into pgvector, ask questions. Clerk JWT auth, per-user documents | Prototype, deployable on Railway |
| `cli-to-saas/production-micro-saas/frontend` | Next.js + Clerk frontend for the Docs Q&A backend | Prototype |
| `lead-qualificatoin-agent` | FastAPI + LangChain agent that scores a lead 1-10 using Tavily web search and Groq | Prototype (no auth, no evaluation) |
| `llm-multiagent-workflow` | LangGraph router that sends input to a lead qualifier, support triage, or human review. Uses a rule-based mock LLM by default | Demo |
| `FlyRankAI`, `index.html` | Static portfolio pages | Static |

The `cli-to-saas` folder follows one idea: the same app grown from a CLI, to an API backend, to a small SaaS with a login.

The folder `lead-qualificatoin-agent` keeps its original (misspelled) name so existing links keep working.

## How the cli-to-saas projects connect

1. `personal-research-assistant-cli`: one LLM call with structured output.
2. `docs-qa-backend`: retrieval over your own uploaded documents.
3. `production-micro-saas/frontend`: a login and UI on top of the backend.

## Notes

- None of these projects has CI yet.
- Evaluation results for the Docs Q&A backend are not published.
- See `CONTRIBUTING.md` for how new case studies are added.
