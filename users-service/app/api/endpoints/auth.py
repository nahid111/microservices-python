from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from app.api.deps import authenticate_user_and_get_token, require_token
from app.db.database import get_db

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login_form_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    return authenticate_user_and_get_token(form_data.username.lower(), form_data.password, db)


@router.post('/token', response_model=schemas.Token)
def login_for_token(payload: schemas.LoginPayload, db: Session = Depends(get_db)):
    res = authenticate_user_and_get_token(payload.email.lower(), payload.password, db)
    return res


@router.get('/token/validate')
def validate_token(email: str = Depends(require_token)):
    return email
