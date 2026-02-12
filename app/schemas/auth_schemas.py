from pydantic import BaseModel

class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class AuthResponseSchema:
    access_token: str
    refresh_token: str
    token_type: str


    def __init__(self, access_token, refresh_token, token_type="bearer"):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type
