import uuid

from app.dto import CredentialsRequest, TokenResponse
from app.exceptions import (
    AccountRequiredError,
    InvalidCredentialsError,
    LoginTakenError,
)
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
        return self._token(str(user.id), user.login, user.is_premium)

    async def login(self, data: CredentialsRequest) -> TokenResponse:
        user = await self._repo.get_by_login(data.login)
        if not user or not verify_password(
            data.password, user.password_hash
        ):
            raise InvalidCredentialsError()
        return self._token(str(user.id), user.login, user.is_premium)

    def guest(self, name: str) -> TokenResponse:
        return self._token(str(uuid.uuid4()), name.strip(), False)

    async def upgrade(self, user_id: str) -> TokenResponse:
        user = await self._repo.get_by_id(user_id)
        if user is None:
            raise AccountRequiredError()
        await self._repo.set_premium(user, True)
        return self._token(str(user.id), user.login, True)

    def _token(
        self, user_id: str, login: str, is_premium: bool
    ) -> TokenResponse:
        token = create_access_token(user_id, login, is_premium)
        return TokenResponse(
            access_token=token,
            user_id=user_id,
            login=login,
            is_premium=is_premium,
        )
