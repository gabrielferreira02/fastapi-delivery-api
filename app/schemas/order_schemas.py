from pydantic import BaseModel
from uuid import UUID
from app.enums.order_status import OrderStatus
from app.models.order_item import OrderItem
from datetime import datetime
from app.schemas.product_schemas import ProductResponseSchema

class ItemSchema(BaseModel):
    id: UUID
    quantity: float

    class Config:
        from_attributes = True

class CreateOrderSchema(BaseModel):
    user_id: UUID
    items: list[ItemSchema]

    class Config:
        from_attributes = True

class OrderItemSchema(BaseModel):
    id: UUID
    quantity: int
    product: ProductResponseSchema


class OrderResponseSchema(BaseModel):
    id: UUID
    user_id: UUID
    total: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemSchema]

    class Config:
        from_attributes = True