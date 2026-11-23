from fastapi import APIRouter
from .homepage import router as homepage_router 
from .forwarder import router as forward_router

main_router = APIRouter()

main_router.include_router(homepage_router)
main_router.include_router(forward_router)