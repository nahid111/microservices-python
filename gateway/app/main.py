from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# origins = [
#     settings.CLIENT_ORIGIN,
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def app_startup():
    pass


@app.on_event("shutdown")
async def app_shutdown():
    # close connection to DB
    pass

# uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
