import requests
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def require_token(token: str = Depends(oauth2_scheme)) -> dict[str, str] | None:
    headers = {'Authorization': f'Bearer {token}'}
    url = f"{settings.USERS_SERVICE_URL}/api/v1/token/validate"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.json())
    return {"token": token, "email": res.json()}
