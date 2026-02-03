from app.models.base import Base
from sqlalchemy import Column, Enum, UUID, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.enums.order_status import OrderStatus
import uuid

class Order(Base):
    __tablename__ = "order_db"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column("user_id", ForeignKey("user_db.id"), nullable=False)
    total = Column("total", Float, default=0, nullable=False)
    status = Column(Enum(OrderStatus, name="status"), nullable=False, default=OrderStatus.OPEN)
    items = relationship("OrderItem", cascade="all, delete")
    created_at = Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __init__(self, user_id, status=OrderStatus.OPEN):
        self.user_id = user_id
        self.status = status

    def calculate_price(self):
        self.total = sum(item.quantity * item.price for item in self.items)