from fastapi import APIRouter, Depends
import redis
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.db.models import User
from app.api.dependencies import get_current_user, get_redis_client
from app.api.orders.schemas import OrderCreate, OrderItem, OrderOut
from app.api.orders.repository import OrderRepository
# from app.celery_tasks.tasks import process_order

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/basket", status_code=201)
async def add_to_basket(
    basket_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis_client),
):
    repo = OrderRepository(db, redis_client)
    await repo.create_basket(current_user.id, basket_data.items)
    return {"message": "Товар добавлен в корзину"}


@router.get("/basket", response_model=List[OrderItem])
async def list_basket(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis_client),
):
    repo = OrderRepository(db, redis_client)
    orders = await repo.get_basket(current_user.id)
    return orders


@router.delete("/basket", status_code=201)
async def delete_basket(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis_client),
):
    repo = OrderRepository(db, redis_client)
    await repo.clear_basket(current_user.id)
    return {"message": "Корзина очищена"}


@router.post("/", response_model=OrderOut, status_code=201)
async def create_order(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis_client),
):
    repo = OrderRepository(db, redis_client)
    order = await repo.create_order(current_user.id)
    await db.refresh(order, ["items"])
    # process_order.delay(order.id)

    return order


@router.get("/", response_model=List[OrderOut])
async def list_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis_client),
):
    repo = OrderRepository(db, redis_client)
    orders = await repo.get_all_orders(current_user.id)
    return orders
