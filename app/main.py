from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import main_router

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version='0.1.0',
)

app.include_router(main_router)