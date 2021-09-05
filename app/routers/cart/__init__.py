from .cart import router as cart_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(cart_router)