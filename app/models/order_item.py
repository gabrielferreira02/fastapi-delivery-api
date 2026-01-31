from app.models.base import Base
from sqlalchemy import Column, UUID, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

class OrderItem(Base):
    __tablename__ = "order_item_db"

    id = Column("id", UUID, primary_key=True)
    order_id = Column("order_id", ForeignKey("order_db.id"), nullable=False)
    product_id = Column("produtc_id", ForeignKey("product_db.id"), nullable=False)
    product = relationship("Product", lazy="joined")
    quantity = Column("quantity", Integer, nullable=False)
    price = Column("price", Float, nullable=False)

    class Config:
        from_attributes = True
    
    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

