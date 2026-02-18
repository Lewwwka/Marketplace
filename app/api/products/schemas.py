from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    price: int = Field(gt=0)
    stock: int = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
    seller_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
