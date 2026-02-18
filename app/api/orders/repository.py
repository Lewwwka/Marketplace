from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from aioredis import from_url
from db.models import Order, OrderItem, Product
from core.config import settings

redis = from_url(settings.REDIS_URL)


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_cart(self, user_id: int, items: List[dict]) -> None:
        cart_key = f"cart:{user_id}"
        pipe = redis.pipeline()
        for item in items:
            await pipe.hset(cart_key, str(item["product_id"]), item["quantity"])
        await pipe.execute()

    async def get_cart(self, user_id: int) -> List[dict]:
        cart_key = f"cart:{user_id}"
        items = await redis.hgetall(cart_key)
        return [{"product_id": int(k), "quantity": int(v)} for k, v in items.items()]

    async def clear_cart(self, user_id: int) -> None:
        cart_key = f"cart:{user_id}"
        await redis.delete(cart_key)

    async def create_order(self, user_id: int) -> Order:
        cart = await self.get_cart(user_id)
        if not cart:
            raise ValueError("Корзина пуста")

        total_price = 0
        order = Order(user_id=user_id, total_price=0, status="pending")
        self.db.add(order)
        await self.db.flush()

        for item in cart:
            product = await self.db.get(Product, item["product_id"])
            if not product or product.stock < item["quantity"]:
                raise ValueError(f"Товар {item['product_id']} закончился")

            order_item = OrderItem(
                order_id=order.id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=product.price,
            )
            self.db.add(order_item)
            total_price += product.price * item["quantity"]
            product.stock -= item["quantity"]

        order.total_price = total_price
        await self.db.flush()
        await self.clear_cart(user_id)
        return order

    async def get_multi(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        result = await self.db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
