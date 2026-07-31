from datetime import UTC, datetime, timedelta

import jwt

from backend.app.core.config import settings

def create_access_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        'sub': subject,
        'exp': expire
    }

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)