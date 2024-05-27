import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.models.order_model import Order
from app.models.product_model import Product
from app.models.user_model import User
from app.models.order_item_model import OrderItem
from sqlalchemy.orm import Session
from app.worker.tasks import process_order

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(scope="module")
def db_session():
    from app.db.session import SessionLocal
    db = SessionLocal()
    yield db
    db.close()

def create_test_user(db: Session) -> User:
    user = User(name="Usuário de Teste", email=f"test_user_{uuid.uuid4()}@example.com", hashed_password="senha123")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_test_product(db: Session, quantity=100) -> Product:
    product = Product(name="Produto de Teste", description="Um produto de teste", price=9.99, quantity_in_stock=quantity)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def test_worker_process_order(db_session):
    """Testa se o worker processa o pedido corretamente"""
    user = create_test_user(db_session)
    product = create_test_product(db_session)
    order = Order(user_id=user.id)
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=1)
    db_session.add(order_item)
    db_session.commit()
    db_session.refresh(order_item)

    # Simula o processamento do pedido pelo worker
    process_order(order.id)

    db_session.refresh(order)
    db_session.refresh(product)
    assert order.status == "processed"
    assert product.quantity_in_stock == 99

def test_worker_process_order_insufficient_quantity(db_session):
    """Testa se o worker lida com quantidade insuficiente em estoque"""
    user = create_test_user(db_session)
    product = create_test_product(db_session, quantity=1)
    order = Order(user_id=user.id)
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=2)
    db_session.add(order_item)
    db_session.commit()
    db_session.refresh(order_item)

    with pytest.raises(Exception, match="Produto fora de estoque ou quantidade insuficiente"):
        process_order(order.id)

    db_session.refresh(order)
    assert order.status == "pending"

def test_worker_process_order_invalid_product(db_session):
    """Testa se o worker lida com um produto inválido"""
    user = create_test_user(db_session)
    order = Order(user_id=user.id)
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    order_item = OrderItem(order_id=order.id, product_id=999999, quantity=1)
    db_session.add(order_item)
    db_session.commit()
    db_session.refresh(order_item)

    with pytest.raises(Exception, match="Produto fora de estoque ou quantidade insuficiente"):
        process_order(order.id)

    db_session.refresh(order)
    assert order.status == "pending"