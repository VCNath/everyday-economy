from dataclasses import dataclass
import logging
from uuid import NAMESPACE_DNS, uuid5

from fastapi import Header, HTTPException
import jwt
from jwt import PyJWKClient

from app.config import get_settings

logger = logging.getLogger(__name__)


@dataclass
class AuthIdentity:
    user_id: str
    email: str
    display_name: str | None = None
    role: str = "user"


def _parse_bearer_token(token: str) -> AuthIdentity | None:
    # Phase 4 local auth scaffold:
    # Bearer demo:<email>[:display_name]
    if not token.startswith("demo:"):
        return None
    raw = token.removeprefix("demo:")
    parts = [part.strip() for part in raw.split(":")]
    if not parts or not parts[0]:
        return None
    email = parts[0].lower()
    display_name = parts[1] if len(parts) > 1 and parts[1] else None
    explicit_role = parts[2].lower() if len(parts) > 2 and parts[2] else None
    role = explicit_role if explicit_role in {"admin", "user"} else ("admin" if email.endswith("@admin.local") else "user")
    return AuthIdentity(
        user_id=str(uuid5(NAMESPACE_DNS, f"everyday-economy:{email}")),
        email=email,
        display_name=display_name,
        role=role,
    )


def _decode_supabase_token(token: str) -> AuthIdentity | None:
    settings = get_settings()
    if not (settings.supabase_jwt_secret or settings.supabase_jwks_url):
        return None

    options = {"verify_aud": bool(settings.supabase_audience)}
    try:
        if settings.supabase_jwks_url:
            signing_key = PyJWKClient(settings.supabase_jwks_url).get_signing_key_from_jwt(token)
            claims = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256", "ES256"],
                audience=settings.supabase_audience,
                issuer=settings.supabase_issuer,
                options=options,
            )
        else:
            claims = jwt.decode(
                token,
                settings.supabase_jwt_secret,
                algorithms=["HS256"],
                audience=settings.supabase_audience,
                issuer=settings.supabase_issuer,
                options=options,
            )
    except jwt.InvalidTokenError as exc:
        logger.info("Invalid Supabase JWT: %s", exc)
        return None

    user_id = claims.get("sub")
    email = claims.get("email")
    metadata = claims.get("user_metadata") or {}
    display_name = (
        metadata.get("display_name")
        or metadata.get("full_name")
        or metadata.get("name")
        or claims.get("name")
    )
    if not user_id or not email:
        return None
    return AuthIdentity(
        user_id=str(user_id),
        email=str(email).lower(),
        display_name=str(display_name) if display_name else None,
        role="user",
    )


def get_current_identity(authorization: str | None = Header(default=None)) -> AuthIdentity:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Authentication required.")
    token = authorization.split(" ", 1)[1].strip()
    settings = get_settings()
    identity = None
    if token.startswith("demo:"):
        if settings.is_production or not settings.allow_demo_auth:
            raise HTTPException(status_code=401, detail="Demo authentication is disabled.")
        identity = _parse_bearer_token(token)
    else:
        identity = _decode_supabase_token(token)
    if identity is None:
        raise HTTPException(status_code=401, detail="Invalid authentication token.")
    return identity
