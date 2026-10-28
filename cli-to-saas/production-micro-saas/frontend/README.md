# Docs Q&A Frontend

Next.js app (App Router) with Clerk sign-in. After signing in, a user can upload a PDF or Markdown file and ask questions about their own documents. It talks to the backend in `../../docs-qa-backend`.

The frontend sends the Clerk session token as a Bearer token on every request. The backend verifies it. A signed-in page alone does not protect data, the backend checks do.

## Setup

```bash
npm install
# create .env.local with the variables below
npm run dev
```

Open http://localhost:3000.

## Environment variables

| Variable | Notes |
|---|---|
| `NEXT_PUBLIC_API_URL` | Backend URL. Defaults to `http://localhost:8000` |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | From your Clerk dashboard |
| `CLERK_SECRET_KEY` | From your Clerk dashboard |

## Backend requirements

The backend must have `ALLOWED_ORIGINS` set to this app's origin (for example `http://localhost:3000`), and `CLERK_JWKS_URL` and `CLERK_ISSUER` set to the same Clerk application. Otherwise requests are blocked by CORS or rejected with 401.

## Files

- `app/page.tsx`, `app/layout.tsx`: landing page and Clerk provider
- `app/components/Dashboard.tsx`: upload and ask UI, adds the token to requests
- `proxy.ts`: Clerk middleware
