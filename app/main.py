from fastapi import FastAPI
from passlib.context import CryptContext

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from app.api.routes.auth_routes import auth_router
from app.api.routes.user_routes import user_router

app.include_router(auth_router)
app.include_router(user_router)