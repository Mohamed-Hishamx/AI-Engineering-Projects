"""
Server-side Clerk JWT verification. Identity comes ONLY from a verified token,
never from the request body.
"""

import jwt
from jwt import PyJWKClient
from fastapi import Header, HTTPException
from src.config import settings

_jwks_client = PyJWKClient(settings.clerk_jwks_url)


def get_current_user_id(authorization: str = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token.")
    token = authorization.split(" ", 1)[1].strip()
    try:
        signing_key = _jwks_client.get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=settings.clerk_issuer,
            options={"require": ["exp", "iss", "sub"], "verify_aud": False},
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return claims["sub"]
