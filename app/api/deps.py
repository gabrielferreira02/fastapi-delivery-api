from sqlalchemy.orm import Session, sessionmaker
from app.models.base import db

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
        