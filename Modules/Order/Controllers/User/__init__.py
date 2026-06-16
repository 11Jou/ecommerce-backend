from fastapi import APIRouter
from .CartController import router as cart_router
from .OrderController import router as order_router

router = APIRouter()

router.include_router(cart_router)
router.include_router(order_router)