from fastapi import APIRouter
from .homepage import router as homepage_router 

main_router = APIRouter()

main_router.include_router(homepage_router)