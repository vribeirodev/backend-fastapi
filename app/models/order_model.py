from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
from app.models.order_item_model import OrderItem  
from app.models.user_model import User  

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='pending')

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

User.orders = relationship("Order", back_populates="user")
