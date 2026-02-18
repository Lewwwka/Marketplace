from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from db.models import Product


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, seller_id: int, **data) -> Product:
        data["seller_id"] = seller_id
        product = Product(**data)
        self.db.add(product)
        await self.db.flush()
        return product

    async def get(self, product_id: int) -> Optional[Product]:
        result = await self.db.execute(
            select(Product).where(Product.id == product_id, Product.is_active is True)
        )
        return result.scalar_one_or_none()

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[Product]:
        result = await self.db.execute(
            select(Product)
            .where(Product.is_active is True)
            .offset(skip)
            .limit(limit)
            .order_by(Product.created_at.desc())
        )
        return result.scalars().all()
