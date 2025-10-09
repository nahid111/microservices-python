from typing import Any, List

import requests
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app import schemas
from app.api.deps import oauth2_scheme
from app.core.config import settings

router = APIRouter()

service_url = f"{settings.USERS_SERVICE_URL}/api/v1/users"


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100) -> Any:
    """Retrieve users."""
    res = requests.get(service_url)
    return JSONResponse(status_code=res.status_code, content=res.json())


@router.post("/", response_model=schemas.User)
def create_user(payload: schemas.UserCreate) -> Any:
    """Create new user."""
    res = requests.post(service_url, json=payload.model_dump())
    return JSONResponse(status_code=res.status_code, content=res.json())


@router.get("/me")
def read_user_me(token: str = Depends(oauth2_scheme)) -> Any:
    """Get current user."""
    res = requests.get(f"{service_url}/me", headers={'Authorization': f'Bearer {token}'})
    return JSONResponse(status_code=res.status_code, content=res.json())
