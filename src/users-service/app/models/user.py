from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """DB model for User"""

    id: int | None = Field(default=None, primary_key=True)
    full_name: str | None = Field(default=None, max_length=100, index=True)
    email: str = Field(max_length=100, index=True, unique=True)
    hashed_password: str = Field(max_length=200)
    created_at: datetime = Field(default_factory=datetime.now)
