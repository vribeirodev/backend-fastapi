from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import User, UserCreate
from app.services import user_service
from app.api.v1 import deps

router = APIRouter()

@router.post("/", response_model=User, summary="Criar um novo usuário", description="Este endpoint permite criar um novo usuário. Forneça o nome do usuário, email e senha.")
def create_user(*, db: Session = Depends(deps.get_db), user_in: UserCreate):
    existing_user = user_service.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso."
        )
    user = user_service.create_user(db=db, user=user_in)
    return user

@router.get("/{user_id}", response_model=User, summary="Obter usuário por ID", description="Recuperar os detalhes de um usuário pelo seu ID.")
def read_user(*, db: Session = Depends(deps.get_db), user_id: int):
    user = user_service.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuário não encontrado")
    return user
