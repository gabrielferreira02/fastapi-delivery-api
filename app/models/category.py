from base import Base
from sqlalchemy import Column, String, UUID

class Category(Base):
    __tablename__ = "category_db"

    id = Column("id", UUID, primary_key=True)
    name = Column("name", String, nullable=False)
    slug = Column("slug", String, nullable=False, unique=True)

    class Config:
        from_attributes=True

    def __init__(self, name, slug):
        self.name = name
        self.slug = slug