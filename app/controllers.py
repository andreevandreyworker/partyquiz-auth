import uuid

from app.dto import CredentialsRequest, TokenResponse
from app.exceptions import InvalidCredentialsError, LoginTakenError
from app.repositories import UserRepository
from app.security import (
    create_access_token,
    hash_password,
    verify_password,
)


class AuthController:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def register(self, data: CredentialsRequest) -> TokenResponse:
        if await self._repo.get_by_login(data.login):
            raise LoginTakenError()
        user = await self._repo.create(
            data.login, hash_password(data.password)
        )
        return self._token(str(user.id), user.login)

    async def login(self, data: CredentialsRequest) -> TokenResponse:
        user = await self._repo.get_by_login(data.login)
        if not user or not verify_password(
            data.password, user.password_hash
        ):
            raise InvalidCredentialsError()
        return self._token(str(user.id), user.login)

    def guest(self, name: str) -> TokenResponse:
        return self._token(str(uuid.uuid4()), name.strip())

    def _token(self, user_id: str, login: str) -> TokenResponse:
        token = create_access_token(user_id, login)
        return TokenResponse(
            access_token=token, user_id=user_id, login=login
        )
