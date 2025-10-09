# ruff: noqa: D101

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    email: str | None = None


class LoginPayload(BaseModel):
    email: EmailStr
    password: str
