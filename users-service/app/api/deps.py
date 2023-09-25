from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import models
from app.core import security
from app.db.database import get_db
from app.utils import credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login", scheme_name="JWT")


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def generate_token(email):
    return {
        "access_token": security.create_access_token(subject=email),
        "refresh_token": security.create_refresh_token(subject=email),
        "token_type": "bearer"
    }


def authenticate_user(email: str, password: str, db: Session):
    """Validate creds"""
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user


def authenticate_user_and_get_token(email: str, password: str, db: Session):
    """Validate creds & return token"""
    user = authenticate_user(email, password, db)
    if not user:
        raise credentials_exception
    if not security.verify_password(password, user.hashed_password):
        raise credentials_exception
    return generate_token(user.email)


def require_token(token: str = Depends(oauth2_scheme)):
    """Function to make route protected"""
    return security.validate_access_token(token)


def require_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Function to make route protected and get current_user"""
    email = security.validate_access_token(token)
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user
