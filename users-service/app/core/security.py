# ruff: noqa: D103, ANN401

from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.exceptions import credentials_exception
from app.core.settings import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

ALGORITHM = 'HS256'


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str | Any, expires_delta: int = None) -> str:
    if expires_delta:
        expire = datetime.now() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRES_IN
        )
    to_encode = {'exp': expire, 'sub': str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(subject: str | Any, expires_delta: int = None) -> str:
    if expires_delta:
        expires_delta = datetime.now() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.now() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRES_IN
        )

    to_encode = {'exp': expires_delta, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY_REFRESH, ALGORITHM)
    return encoded_jwt


def validate_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception from JWTError
