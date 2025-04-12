from fastapi import APIRouter

from .records import router as records_router

api_router = APIRouter()
api_router.include_router(records_router, prefix="/records/v1", tags=["독서 기록"])
