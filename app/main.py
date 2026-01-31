from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

app = FastAPI()