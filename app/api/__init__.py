from fastapi import APIRouter
from app.api.routes.read import router as read_router

api_router = APIRouter()
api_router.include_router(read_router)