from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.services import order_service
from app.api.v1 import deps
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Order, summary="Criar um novo pedido", description="Este endpoint permite criar um novo pedido. Forneça o ID do usuário e uma lista de itens do pedido.")
def create_order(*, db: Session = Depends(deps.get_db), order_in: schemas.OrderCreate):
    try:
        order = order_service.create_order(db=db, order_in=order_in)
        return order
    except order_service.ProductNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except order_service.InsufficientQuantityException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{order_id}", response_model=schemas.Order, summary="Obter pedido por ID", description="Recuperar os detalhes de um pedido pelo seu ID.")
def read_order(*, db: Session = Depends(deps.get_db), order_id: int):
    order = order_service.get_order(db=db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

@router.get("/user/{user_id}", response_model=List[schemas.Order], summary="Obter pedidos por ID do usuário", description="Recuperar todos os pedidos feitos por um usuário específico.")
def read_orders_by_user(*, db: Session = Depends(deps.get_db), user_id: int):
    orders = order_service.get_orders_by_user(db=db, user_id=user_id)
    return orders
