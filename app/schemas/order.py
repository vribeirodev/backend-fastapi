from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from .order_item import OrderItem, OrderItemCreate

class OrderBase(BaseModel):
    user_id: int = Field(..., description="ID do usuário que fez o pedido.", example=1)

class OrderCreate(OrderBase):
    items: List[OrderItemCreate] = Field(..., description="Lista de itens do pedido.")

class Order(OrderBase):
    id: int = Field(..., description="ID único do pedido.", example=1)
    created_date: datetime = Field(..., description="Data de criação do pedido.", example="2023-05-26T22:25:27.607Z")
    status: str = Field(..., description="Status do pedido.", example="pending")
    items: List[OrderItem] = Field(..., description="Lista de itens do pedido.")

    class Config:
        from_attributes = True
