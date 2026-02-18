from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import User
from app.core.security import verify_password


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.db.execute(select(User).where(User.email == email))
        user = user.scalar_one_or_none()

        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
