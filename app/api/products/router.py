from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.exceptions import NotFoundException
from app.db.database import get_db
from app.db.models import User
from app.api.dependencies import get_current_user
from app.api.products.schemas import ProductCreate, ProductOut
from app.api.products.repository import ProductRepository

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductOut, status_code=201)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ProductRepository(db)
    product = await repo.create(seller_id=current_user.id, **product_data.model_dump())
    return product


@router.get("/", response_model=List[ProductOut])
async def list_products(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    repo = ProductRepository(db)
    products = await repo.get_multi(skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    product = await repo.get(product_id)
    if not product:
        raise NotFoundException(product)
    return product
