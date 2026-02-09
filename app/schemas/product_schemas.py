from pydantic import BaseModel
from uuid import UUID

class ProductResponseSchema(BaseModel):
    id: UUID
    name: str
    slug: str
    description: str
    price: float
    image_url: str
    category_id: UUID
    is_active: bool

    class Config:
        from_attributes = True

class UpdateProductSchema(BaseModel):
    name: str
    slug: str
    description: str
    price: float
    category_id: UUID

    class Config:
        from_attributes = True