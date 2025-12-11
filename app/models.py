from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base # Import Base từ database.py

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("Item", back_populates="order")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_code = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    order = relationship("Order", back_populates="items")
    images = relationship("ItemImage", back_populates="item")

class ItemImage(Base):
    __tablename__ = "item_images"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    file_name = Column(String, index=True, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    item = relationship("Item", back_populates="images")