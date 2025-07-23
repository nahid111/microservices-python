from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.core.dependencies import require_current_user, require_token
from app.core.security import get_password_hash
from app.db import get_session
from app.models import User


router = APIRouter()


@router.get('/', response_model=list[schemas.User])
def read_users(
    db: Annotated[Session, Depends(get_session)],
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    """Retrieve users."""
    users = db.query(User).limit(limit).offset(skip).all()
    return users


@router.post('/', response_model=schemas.User)
def create_user(
    payload: schemas.UserCreate, db: Annotated[Session, Depends(get_session)]
) -> User:
    """Create new user."""
    user = db.query(User).filter(User.email == payload.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail='Record already exists.',
        )
    hp = get_password_hash(payload.password)
    user = User(
        email=payload.email, hashed_password=hp, full_name=payload.full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete('/{user_id}')
def delete_user(
    user_id: int,
    db: Annotated[Session, Depends(get_session)],
    email: Annotated[str, Depends(require_token)],
) -> str:
    """Delete a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(user)
    db.commit()
    return 'user Deleted'


@router.get('/me', response_model=schemas.User)
def read_user_me(
    current_user: Annotated[User, Depends(require_current_user)],
) -> User:
    """Get current user."""
    return current_user
