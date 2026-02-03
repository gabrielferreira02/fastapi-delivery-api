from pydantic import BaseModel
from uuid import UUID

class UserResponseSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True