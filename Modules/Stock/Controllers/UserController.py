from Modules.Stock.Services.CategoryService import CategoryService, get_category_service
from Modules.Stock.Services.ProductService import ProductService, get_product_service
from Modules.Stock.Schemas import CategorySchema, ProductSchema
from fastapi import Depends
from Modules.Auth.CheckAuth import get_current_user
from Modules.Auth.Models import User
from typing import List
from fastapi import APIRouter
from Utils.Response import success_response
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/stock", tags=["stock"])

@router.get("/categories")
def get_all_categories_controller(
    current_user: User = Depends(get_current_user),
    category_service: CategoryService = Depends(get_category_service)
    ) -> JSONResponse:
    categories = category_service.get_all_categories()
    return success_response(message="Categories fetched successfully", data=categories, status_code=200)

@router.get("/categories/{category_id}")
def get_category_by_id_controller(
    category_id: int,
    current_user: User = Depends(get_current_user),
    category_service: CategoryService = Depends(get_category_service)
    ) -> JSONResponse:
    category = category_service.get_category_by_id(category_id)
    return success_response(message="Category fetched successfully", data=category, status_code=200)


@router.get("/products")
def get_all_products_controller(
    current_user: User = Depends(get_current_user),
    product_service: ProductService = Depends(get_product_service)
    ) -> JSONResponse:
    products = product_service.get_active_products_with_availability()
    return success_response(message="Products fetched successfully", data=products, status_code=200)


@router.get("/products/{product_id}")
def get_product_by_id_controller(
    product_id: int,
    current_user: User = Depends(get_current_user),
    product_service: ProductService = Depends(get_product_service)
    ) -> JSONResponse:
    product = product_service.get_product_by_id_with_availability(product_id)
    return success_response(message="Product fetched successfully", data=product, status_code=200)
