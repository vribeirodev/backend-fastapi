from pydantic import BaseModel, Field
from decimal import Decimal

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nome do produto. Deve ter entre 1 e 100 caracteres.", example="Celular")
    description: str = Field(..., min_length=1, description="Descrição do produto.", example="Smartphone com 64GB de armazenamento.")
    price: Decimal = Field(..., gt=0, description="Preço do produto. Deve ser um valor positivo.", example=1999.99)
    quantity_in_stock: int = Field(..., ge=0, description="Quantidade do produto em estoque. Deve ser um valor maior ou igual a zero.", example=50)

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int = Field(..., description="ID único do produto.", example=1)

    class Config:
        from_attributes = True