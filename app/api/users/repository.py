from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from db.models import User
from core.security import get_password_hash


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, email: str, password: str, full_name: str = None) -> User:
        hashed_password = get_password_hash(password)
        user = User(email=email, hashed_password=hashed_password, full_name=full_name)
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def update(self, user: User, **kwargs) -> User:
        if "password" in kwargs:
            kwargs["hashed_password"] = get_password_hash(kwargs.pop("password"))
        for key, value in kwargs.items():
            setattr(user, key, value)
        await self.db.flush()
        return user

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
