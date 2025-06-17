from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: Optional[str] = Field(default=None, max_length=100, index=True)
    email: str = Field(max_length=100, index=True, unique=True)
    hashed_password: str = Field(max_length=200)
    created_at: datetime = Field(default_factory=datetime.now)
