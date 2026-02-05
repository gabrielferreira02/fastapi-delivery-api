from pydantic import BaseModel
from uuid import UUID

class CategoryResponseSchema(BaseModel):
    id: UUID
    name: str
    slug: str
    image_url: str

    class Config:
        from_attributes = True

class UpdateCategoryNameAndSlugSchema(BaseModel):
    name: str
    slug: str

    class Config:
        from_attributes = True