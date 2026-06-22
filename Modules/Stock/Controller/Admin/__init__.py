from fastapi import APIRouter

from .CategoryController import router as category_router
from .ProductController import router as product_router
from .StockController import router as stock_router
from .StoreController import router as store_router

router = APIRouter()

router.include_router(category_router)
router.include_router(product_router)
router.include_router(store_router)
router.include_router(stock_router)
