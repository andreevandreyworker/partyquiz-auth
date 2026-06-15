from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_login(self, login: str) -> User | None:
        return await self._session.scalar(
            select(User).where(User.login == login)
        )

    async def create(self, login: str, password_hash: str) -> User:
        user = User(login=login, password_hash=password_hash)
        self._session.add(user)
        await self._session.flush()
        return user
