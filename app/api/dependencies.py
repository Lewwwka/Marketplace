from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.redus_client import get_redis
from app.db.models import User
from app.db.database import get_db
from app.core.security import verify_token
from app.core.exceptions import (
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = await verify_token(credentials.credentials)
    if payload is None:
        raise UnauthorizedException()

    email = payload.get("sub")
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if user is None:
        raise NotFoundException("Пользователя")

    if not getattr(user, "is_active", True):
        raise ForbiddenException()

    return user


async def get_redis_client() -> redis.Redis:
    return await get_redis()
