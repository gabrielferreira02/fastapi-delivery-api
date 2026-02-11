from fastapi import APIRouter, Depends
from uuid import UUID
from app.api.deps import get_session
from sqlalchemy.orm import Session
from app.services.order_service import OrderService
from app.schemas.order_schemas import CreateOrderSchema, OrderResponseSchema

order_router = APIRouter(prefix="/order", tags=["Orders"])

@order_router.post("", response_model=OrderResponseSchema)
async def create_order(body: CreateOrderSchema, session: Session = Depends(get_session)):
    return OrderService.create_order(body, session)

@order_router.get("{id}", response_model=OrderResponseSchema)
async def get_order_by_id(id: UUID, session: Session = Depends(get_session)):
    return OrderService.get_order_by_id(id, session)

@order_router.get("user/{id}", response_model=list[OrderResponseSchema])
async def get_user_orders(id: UUID, session: Session = Depends(get_session)):
    return OrderService.list_user_orders(id, session)

@order_router.patch("{id}/cancel", response_model=OrderResponseSchema)
async def cancel_order(id: UUID, session: Session = Depends(get_session)):
    return OrderService.cancel_order(id, session)

@order_router.patch("{id}/delivered", response_model=OrderResponseSchema)
async def delivery_order(id: UUID, session: Session = Depends(get_session)):
    return OrderService.delivered_order(id, session)