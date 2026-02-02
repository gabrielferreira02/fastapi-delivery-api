from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

app = FastAPI()

from app.api.routes.auth_routes import auth_router

app.include_router(auth_router)