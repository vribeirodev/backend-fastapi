from sqlalchemy.orm import Session
from app.models.order_model import Order
from app.models.order_item_model import OrderItem
from app.models.product_model import Product
from app.schemas.order import OrderCreate
from datetime import datetime
from app.worker.tasks import process_order

class ProductNotFoundException(Exception):
    pass

class InsufficientQuantityException(Exception):
    pass

def create_order(db: Session, order_in: OrderCreate) -> Order:
    db_order = Order(
        user_id=order_in.user_id,
        created_date=datetime.utcnow(),
        status='pending'
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise ProductNotFoundException(f"Produto com id {item.product_id} não encontrado")
        if product.quantity_in_stock < item.quantity:
            raise InsufficientQuantityException(f"Quantidade insuficiente em estoque para o produto {item.product_id}")
        
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(db_order_item)
        db.commit()
        db.refresh(db_order_item)

    process_order.delay(db_order.id)

    return db_order

def get_order(db: Session, order_id: int) -> Order:
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()

def get_orders_by_user(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()
