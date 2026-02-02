from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_session
from app.services.auth_service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register")
async def register(session: Session = Depends(get_session)):
    AuthService.register(session)
    pass

@auth_router.post("/login")
async def login(session: Session = Depends(get_session)):
    AuthService.login(session)
    pass

@auth_router.post("/refresh")
async def refresh_token(session: Session = Depends(get_session)):
    AuthService.refresh_token(session)
    pass

@auth_router.post("/forgot-password")
async def forgot_password(session: Session = Depends(get_session)):
    AuthService.forgot_password(session)
    pass