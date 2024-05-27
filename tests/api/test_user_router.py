import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

def test_create_user(client):
    """Testa a criação de um novo usuário"""
    unique_email = f"test_{uuid.uuid4()}@example.com"
    response = client.post("/api/v1/users/", json={"name": "Test User", "email": unique_email, "password": "password123"})
    assert response.status_code == 200
    assert response.json()["email"] == unique_email

def test_read_user(client):
    """Testa a leitura de um usuário existente"""
    unique_email = f"test_{uuid.uuid4()}@example.com"
    create_response = client.post("/api/v1/users/", json={"name": "Test User", "email": unique_email, "password": "password123"})
    assert create_response.status_code == 200
    user_id = create_response.json()["id"]

    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == unique_email

def test_create_user_duplicate_email(client):
    """Testa a criação de um usuário com um email já existente"""
    unique_email = f"test_{uuid.uuid4()}@example.com"
    response = client.post("/api/v1/users/", json={"name": "Test User", "email": unique_email, "password": "password123"})
    assert response.status_code == 200

    duplicate_response = client.post("/api/v1/users/", json={"name": "Test User", "email": unique_email, "password": "password123"})
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Email já está em uso."

def test_create_user_invalid_email(client):
    """Testa a criação de um usuário com um email inválido"""
    invalid_email = "invalid-email"
    response = client.post("/api/v1/users/", json={"name": "Test User", "email": invalid_email, "password": "password123"})
    assert response.status_code == 422  # Unprocessable Entity

def test_create_user_short_password(client):
    """Testa a criação de um usuário com uma senha curta"""
    unique_email = f"test_{uuid.uuid4()}@example.com"
    response = client.post("/api/v1/users/", json={"name": "Test User", "email": unique_email, "password": "short"})
    assert response.status_code == 422  # Unprocessable Entity

def test_create_user_short_name(client):
    """Testa a criação de um usuário com um nome curto"""
    unique_email = f"test_{uuid.uuid4()}@example.com"
    response = client.post("/api/v1/users/", json={"name": "", "email": unique_email, "password": "password123"})
    assert response.status_code == 422  # Unprocessable Entity

def test_read_user_not_found(client):
    """Testa a leitura de um usuário não existente"""
    response = client.get("/api/v1/users/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"
