from fastapi import APIRouter
from .available import router as available_router

router = APIRouter(prefix='/api/v1')

router.include_router(available_router, tags=['available'])

