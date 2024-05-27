import logging
from app.core.celery_app import celery_app
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.order_model import Order
from app.models.order_item_model import OrderItem
from app.models.product_model import Product

@celery_app.task(name="app.worker.tasks.process_order")
def process_order(order_id: int):
    logging.info(f"Processando pedido {order_id}")
    db: Session = SessionLocal()

    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            logging.error(f"Pedido {order_id} não encontrado")
            return
        
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product and product.quantity_in_stock >= item.quantity:
                product.quantity_in_stock -= item.quantity
            else:
                logging.error(f"Produto {item.product_id} fora de estoque ou quantidade insuficiente")
                raise Exception("Produto fora de estoque ou quantidade insuficiente")
        
        order.status = "processed"
        db.commit()
        logging.info(f"Pedido {order_id} processado com sucesso")
    except Exception as e:
        db.rollback()
        logging.error(f"Erro ao processar pedido {order_id}: {e}")
        raise e
    finally:
        db.close()