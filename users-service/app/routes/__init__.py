from fastapi import APIRouter

from app.routes import auth, users


api_router = APIRouter()
api_router.include_router(auth.router, prefix='/api/v1', tags=['auth'])
api_router.include_router(users.router, prefix='/api/v1/users', tags=['users'])
