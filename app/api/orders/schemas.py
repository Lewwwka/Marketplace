from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime


class OrderItem(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItem]


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: int


class OrderOut(BaseModel):
    id: int
    user_id: int
    total_price: int
    status: str
    items: List[OrderItemOut]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
