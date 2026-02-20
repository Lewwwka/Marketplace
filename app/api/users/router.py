from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlredyRegisterException
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.db.models import User
from app.api.users.schemas import UserCreate, UserUpdate, UserOut
from app.api.users.repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut, status_code=201)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    existing = await repo.get_by_email(user_data.email)
    if existing:
        raise AlredyRegisterException()

    user = await repo.create(user_data.email, user_data.password, user_data.full_name)
    return user


@router.get("/me", response_model=UserOut)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut)
async def update_user_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = UserRepository(db)
    user = await repo.update(current_user, **user_data.model_dump(exclude_unset=True))
    return user


@router.delete("/me", status_code=204)
async def delete_user_me(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = UserRepository(db)
    await repo.delete_me(user)
    return None
