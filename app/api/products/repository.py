from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.models import Product


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, seller_id: int, **data) -> Product:
        data["seller_id"] = seller_id
        product = Product(**data)
        self.db.add(product)
        await self.db.flush()
        return product

    async def get_all(self) -> List[Product]:
        result = await self.db.execute(
            select(Product).order_by(Product.created_at.desc())
        )
        return result.scalars().all()

    async def get_by_name(self, product_name: str) -> List[Product]:
        result = await self.db.execute(
            select(Product)
            .where(Product.name == product_name)
            .order_by(Product.created_at.desc())
        )
        return result.scalars().all()
