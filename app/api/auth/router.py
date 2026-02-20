from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedException
from app.db.database import get_db
from app.core.security import create_access_token
from app.api.auth.schemas import LoginRequest, LoginResponse
from app.api.auth.repository import AuthRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(form_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    repo = AuthRepository(db)
    user = await repo.authenticate(form_data.email, form_data.password)

    if not user:
        raise UnauthorizedException()

    access_token = create_access_token(user.email)

    return LoginResponse(
        access_token=access_token,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
        },
    )
