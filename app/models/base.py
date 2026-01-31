from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from app.main import DB_URL

db = create_engine(DB_URL)
Base = declarative_base()