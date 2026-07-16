import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.config import get_settings


security = HTTPBasic()


def authenticate_user(
    credentials: HTTPBasicCredentials = Depends(security),
) -> str:
    settings = get_settings()

    username_is_valid = secrets.compare_digest(
        credentials.username,
        settings.api_username,
    )

    password_is_valid = secrets.compare_digest(
        credentials.password,
        settings.api_password,
    )

    if not username_is_valid or not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username