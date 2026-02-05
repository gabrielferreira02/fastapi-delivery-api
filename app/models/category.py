from app.models.base import Base
from sqlalchemy import Column, String, UUID
import uuid

class Category(Base):
    __tablename__ = "category_db"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column("name", String, nullable=False)
    slug = Column("slug", String, nullable=False, unique=True)
    image_url = Column("image_url", String, nullable=False)

    def __init__(self, name, slug, image_url):
        self.name = name
        self.slug = slug
        self.image_url = image_url