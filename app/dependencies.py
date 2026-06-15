import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.controllers import AuthController
from app.db import get_session
from app.dto import UserResponse
from app.exceptions import NotAuthenticatedError
from app.repositories import UserRepository

bearer = HTTPBearer(auto_error=False)


def get_controller(
    session: AsyncSession = Depends(get_session),
) -> AuthController:
    return AuthController(UserRepository(session))


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> UserResponse:
    if creds is None:
        raise NotAuthenticatedError()
    try:
        payload = jwt.decode(
            creds.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.PyJWTError:
        raise NotAuthenticatedError()
    return UserResponse(
        user_id=payload["sub"],
        login=payload["login"],
        is_premium=payload.get("premium", False),
    )
