from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from app.api.v1.routers import user, product, order
from app.db.session import SessionLocal, engine
from app.db.base import Base  # Importa a Base que contém os modelos
from app.initial_data import init_db
import subprocess

app = FastAPI(
    title="Loja Virtual API - (Projeto Teste Backend VOLUS)",
    description="API para gerenciar uma loja virtual, incluindo usuários, produtos e pedidos.",
    version="0.1.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"loc": err["loc"], "msg": err["msg"], "type": err["type"]} for err in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={"detail": "Erro de validação", "errors": errors}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(IntegrityError)
async def db_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Erro de banco de dados", "errors": str(exc)}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocorreu um erro inesperado."}
    )

@app.on_event("startup")
def on_startup():
    # Aplica as migrações do Alembic
    result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Erro durante a aplicação da migração: {result.stderr}")

    # Pre-popular o banco de dados
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(product.router, prefix="/api/v1/products", tags=["products"])
app.include_router(order.router, prefix="/api/v1/orders", tags=["orders"])