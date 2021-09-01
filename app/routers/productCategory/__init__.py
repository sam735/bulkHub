from .productCategory import router as product_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(product_router)