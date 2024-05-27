import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.product_model import Product

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(scope="module")
def db_session():
    from app.db.session import SessionLocal
    db = SessionLocal()
    yield db
    db.close()

def create_test_user(db: Session):
    unique_email = f"user_{uuid.uuid4()}@example.com"
    user = User(name="Test User", email=unique_email, hashed_password="hashedpassword")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_test_product(db: Session):
    product = Product(name="Test Product", description="Test Description", price=100.0, quantity_in_stock=10)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def test_create_order(client, db_session):
    """Testa a criação de um novo pedido"""
    user = create_test_user(db_session)
    product = create_test_product(db_session)
    response = client.post("/api/v1/orders/", json={
        "user_id": user.id,
        "items": [{"product_id": product.id, "quantity": 1}]
    })
    assert response.status_code == 200
    assert response.json()["user_id"] == user.id

def test_read_order(client, db_session):
    """Testa a leitura de um pedido existente"""
    user = create_test_user(db_session)
    product = create_test_product(db_session)
    create_response = client.post("/api/v1/orders/", json={
        "user_id": user.id,
        "items": [{"product_id": product.id, "quantity": 1}]
    })
    assert create_response.status_code == 200
    order_id = create_response.json()["id"]

    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id

def test_read_orders_by_user(client, db_session):
    """Testa a leitura de pedidos por ID do usuário"""
    user = create_test_user(db_session)
    product = create_test_product(db_session)
    client.post("/api/v1/orders/", json={
        "user_id": user.id,
        "items": [{"product_id": product.id, "quantity": 1}]
    })
    response = client.get(f"/api/v1/orders/user/{user.id}")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_order_invalid_product(client, db_session):
    """Testa a criação de um pedido com um ID de produto inválido"""
    user = create_test_user(db_session)
    response = client.post("/api/v1/orders/", json={
        "user_id": user.id,
        "items": [{"product_id": 999999, "quantity": 1}]
    })
    assert response.status_code == 400

def test_create_order_insufficient_quantity(client, db_session):
    """Testa a criação de um pedido com quantidade de produto insuficiente"""
    user = create_test_user(db_session)
    product = create_test_product(db_session)
    response = client.post("/api/v1/orders/", json={
        "user_id": user.id,
        "items": [{"product_id": product.id, "quantity": 100}]
    })
    assert response.status_code == 400

def test_read_order_not_found(client):
    """Testa a leitura de um pedido que não existe"""
    response = client.get("/api/v1/orders/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado"
