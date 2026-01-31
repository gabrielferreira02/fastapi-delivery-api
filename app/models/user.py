from app.models.base import Base
from sqlalchemy import Column, String, UUID, DateTime
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "user_db"

    id = Column("id", UUID, primary_key=True)
    first_name = Column("first_name", String, nullable=False)
    last_name = Column("last_name", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False)

    class Config:
        from_attributes = True
    
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
