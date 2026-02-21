import redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


from app.db.models import Order, OrderItem, Product


class OrderRepository:
    def __init__(self, db: AsyncSession, redis_client: redis.Redis):
        self.db = db
        self.redis = redis_client

    async def create_basket(self, user_id: int, items: List[dict]) -> None:
        basket_key = f"basket:{user_id}"
        pipe = self.redis.pipeline()

        for item in items:
            pipe.hset(basket_key, str(item.product_id), str(item.quantity))

        pipe.expire(basket_key, 24 * 60 * 60)
        await pipe.execute()

    async def get_basket(self, user_id: int) -> List[dict]:
        basket_key = f"basket:{user_id}"
        items = await self.redis.hgetall(basket_key)
        return [{"product_id": int(k), "quantity": int(v)} for k, v in items.items()]

    async def clear_basket(self, user_id: int) -> None:
        basket_key = f"basket:{user_id}"
        await self.redis.delete(basket_key)

    async def create_order(self, user_id: int) -> Order:
        basket = await self.get_basket(user_id)
        if not basket:
            raise ValueError("Корзина пуста")

        total_price = 0
        order = Order(user_id=user_id, total_price=0, status="pending")
        self.db.add(order)
        await self.db.flush()

        for item in basket:
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
        await self.clear_basket(user_id)
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
