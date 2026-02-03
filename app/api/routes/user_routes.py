from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_session
from app.services.user_service import UserService
from uuid import UUID
from app.schemas.user_schemas import UserResponseSchema

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.get("{id}", response_model=UserResponseSchema)
async def get_user_data(id: UUID, session: Session = Depends(get_session)):
    return UserService.get_user_data(id, session)

@user_router.delete("{id}")
async def delete_account(id: UUID, session: Session = Depends(get_session)):
    return UserService.delete_account(id, session)