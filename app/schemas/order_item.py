from pydantic import BaseModel, Field

class OrderItemBase(BaseModel):
    product_id: int = Field(..., description="ID do produto.", example=1)
    quantity: int = Field(..., gt=0, description="Quantidade do produto. Deve ser um valor maior que zero.", example=2)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int = Field(..., description="ID único do item do pedido.", example=1)

    class Config:
        from_attributes = True