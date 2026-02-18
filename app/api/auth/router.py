from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.security import create_access_token
from .schemas import LoginRequest, LoginResponse
from .repository import AuthRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(form_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    repo = AuthRepository(db)
    user = await repo.authenticate(form_data.email, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный email или пароль",
        )

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
