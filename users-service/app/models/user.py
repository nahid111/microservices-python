from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(length=100), index=True)
    email = Column(String(length=100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=200), nullable=False)
