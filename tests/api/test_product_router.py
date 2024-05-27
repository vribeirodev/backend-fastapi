import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from decimal import Decimal

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

def test_create_product(client):
    """Testa a criação de um novo produto"""
    response = client.post("/api/v1/products/", json={
        "name": "Celular",
        "description": "Smartphone com 64GB de armazenamento.",
        "price": 1999.99,
        "quantity_in_stock": 50
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Celular"

def test_read_product(client):
    """Testa a leitura de um produto existente"""
    create_response = client.post("/api/v1/products/", json={
        "name": "Celular",
        "description": "Smartphone com 64GB de armazenamento.",
        "price": 1999.99,
        "quantity_in_stock": 50
    })
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Celular"

def test_create_product_invalid_price(client):
    """Testa a criação de um produto com preço inválido"""
    response = client.post("/api/v1/products/", json={
        "name": "Celular",
        "description": "Smartphone com 64GB de armazenamento.",
        "price": -1999.99,
        "quantity_in_stock": 50
    })
    assert response.status_code == 422

def test_create_product_invalid_quantity(client):
    """Testa a criação de um produto com quantidade inválida"""
    response = client.post("/api/v1/products/", json={
        "name": "Celular",
        "description": "Smartphone com 64GB de armazenamento.",
        "price": 1999.99,
        "quantity_in_stock": -50
    })
    assert response.status_code == 422

def test_create_product_missing_fields(client):
    """Testa a criação de um produto com campos faltando"""
    response = client.post("/api/v1/products/", json={
        "name": "Celular"
    })
    assert response.status_code == 422

def test_read_product_not_found(client):
    """Testa a leitura de um produto que não existe"""
    response = client.get("/api/v1/products/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"
