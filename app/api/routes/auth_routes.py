from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_session, verify_token
from app.services.auth_service import AuthService
from app.schemas.auth_schemas import RegisterSchema, LoginSchema
from app.schemas.user_schemas import UserResponseSchema
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=UserResponseSchema)
async def register(body: RegisterSchema, session: Session = Depends(get_session)):
    return AuthService.register(body, session)

@auth_router.post("/login")
async def login(body: LoginSchema, session: Session = Depends(get_session)):
    return AuthService.login(body, session)

@auth_router.post("/refresh")
async def refresh_token(user: User = Depends(verify_token)):
    return AuthService.refresh_token(user)

@auth_router.post("/login-docs")
async def login_docs(body: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    return AuthService.login_docs(body, session)