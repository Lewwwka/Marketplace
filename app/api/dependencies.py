from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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
    email = await verify_token(credentials.credentials)
    if email is None:
        raise UnauthorizedException()

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if user is None:
        raise NotFoundException(user)

    if not user.is_active:
        raise ForbiddenException()

    return user
