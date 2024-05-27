from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nome do usuário. Deve ter entre 1 e 100 caracteres.", example="João da Silva")
    email: EmailStr = Field(..., pattern=r'^\S+@\S+\.\S+$', description="Email do usuário. Deve ser um email válido.", example="joao.silva@example.com")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Senha do usuário. Deve ter no mínimo 8 caracteres.", example="minhasenha123")

class User(UserBase):
    id: int = Field(..., description="ID único do usuário.", example=1)

    class Config:
        from_attributes = True
