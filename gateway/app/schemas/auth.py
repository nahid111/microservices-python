from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class LoginPayload(BaseModel):
    email: EmailStr
    password: str
