from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.db.models import User
from app.api.dependencies import get_current_user
from app.api.orders.schemas import OrderCreate, OrderOut
from app.api.orders.repository import OrderRepository
from app.celery_tasks.tasks import process_order

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/cart", status_code=201)
async def add_to_cart(
    cart_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = OrderRepository(db)
    await repo.create_cart(current_user.id, cart_data.items)
    return {"message": "Корзина обновлена"}


@router.post("/", response_model=OrderOut, status_code=201)
async def create_order(
    cart_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = OrderRepository(db)
    order = await repo.create_order(current_user.id)

    process_order.delay(order.id)

    return order


@router.get("/", response_model=List[OrderOut])
async def list_orders(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = OrderRepository(db)
    orders = await repo.get_multi(user_id=current_user.id)
    return orders
