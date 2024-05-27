from sqlalchemy.orm import Session
from app.models.product_model import Product

def init_db(db: Session) -> None:
    initial_products = [
        {"name": "Produto 1", "description": "Descrição produto 1", "price": 10.0, "quantity_in_stock": 10},
        {"name": "Produto 2", "description": "Descrição produto 2", "price": 20.0, "quantity_in_stock": 20},
        {"name": "Produto 3", "description": "Descrição produto 3", "price": 30.0, "quantity_in_stock": 30},
        {"name": "Produto 4", "description": "Descrição produto 4", "price": 40.0, "quantity_in_stock": 40},
        {"name": "Produto 5", "description": "Descrição produto 5", "price": 50.0, "quantity_in_stock": 50}
    ]
    
    for product_data in initial_products:
        product = db.query(Product).filter(Product.name == product_data["name"]).first()
        if not product:
            product = Product(**product_data)
            db.add(product)
    db.commit()
