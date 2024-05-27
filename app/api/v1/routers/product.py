from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.services import product_service
from app.api.v1 import deps

router = APIRouter()

@router.post("/", response_model=schemas.Product, summary="Criar um novo produto", description="Este endpoint permite criar um novo produto. Forneça o nome do produto, descrição, preço e quantidade em estoque.")
def create_product(*, db: Session = Depends(deps.get_db), product_in: schemas.ProductCreate):
    product = product_service.create_product(db=db, product=product_in)
    return product

@router.get("/{product_id}", response_model=schemas.Product, summary="Obter produto por ID", description="Recuperar os detalhes de um produto pelo seu ID.")
def read_product(*, db: Session = Depends(deps.get_db), product_id: int):
    product = product_service.get_product(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product
