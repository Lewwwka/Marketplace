from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from dependencies import get_current_user
from db.models import User
from schemas import UserCreate, UserUpdate, UserOut
from repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut, status_code=201)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    existing = await repo.get_by_email(user_data.email)
    if existing:
        raise HTTPException(400, "Этот email уже зарегистрирован")

    user = await repo.create(user_data.email, user_data.password, user_data.full_name)
    return user


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut)
async def update_users_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = UserRepository(db)
    user = await repo.update(current_user, **user_data.model_dump(exclude_unset=True))
    return user
