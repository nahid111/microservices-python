from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.core.security import get_password_hash
from app.db.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """Retrieve users."""
    users = db.query(models.User).limit(limit).offset(skip).all()
    return users


@router.post("/", response_model=schemas.User)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)) -> Any:
    """Create new user."""
    user = db.query(models.User).filter(
        models.User.email == payload.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Record already exists.", )
    hp = get_password_hash(payload.password)
    user = models.User(email=payload.email, hashed_password=hp,
                       full_name=payload.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), email: str = Depends(deps.require_token)) -> Any:
    """Delete a user."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return "user Deleted"


@router.get("/me", response_model=schemas.User)
def read_user_me(current_user: models.User = Depends(deps.require_current_user)) -> Any:
    """Get current user."""
    return current_user
