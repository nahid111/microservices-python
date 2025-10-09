import requests
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app import schemas
from app.core.config import settings

router = APIRouter()


@router.post('/token', response_model=schemas.Token)
def login_for_token(payload: schemas.LoginPayload):
    res = requests.post(f"{settings.USERS_SERVICE_URL}/api/v1/token", json=payload.model_dump())
    return JSONResponse(status_code=res.status_code, content=res.json())
