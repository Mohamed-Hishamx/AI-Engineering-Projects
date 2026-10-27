import os

# Required settings must be provided explicitly for tests (no silent fallbacks in src/config.py).
os.environ.setdefault("GROQ_API_KEY", "test-key")
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/docsqa_test")
os.environ.setdefault("CLERK_JWKS_URL", "https://example.clerk.test/.well-known/jwks.json")
os.environ.setdefault("CLERK_ISSUER", "https://example.clerk.test")
os.environ.setdefault("ALLOWED_ORIGINS", "http://localhost:3000")
