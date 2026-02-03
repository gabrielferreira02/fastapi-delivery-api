from app.models.base import Base
from sqlalchemy import Column, UUID, String, Float, Boolean, ForeignKey
import uuid

class Product(Base):
    __tablename__ = "product_db"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column("name", String, nullable=False)
    slug = Column("slug", String, nullable=False)
    description = Column("description", String, nullable=False)
    price = Column("price", Float, nullable=False)
    category_id = Column("category_id", ForeignKey("category_db.id"), nullable=False)
    is_active = Column("is_active", Boolean, default=True)
    image_url = Column("image_url", String)

    def __init__(self, name, slug, description, price, category_id, is_active=True):
        self.name = name
        self.slug = slug
        self.description = description
        self.price = price
        self.category_id = category_id
        self.is_active = is_active
    


