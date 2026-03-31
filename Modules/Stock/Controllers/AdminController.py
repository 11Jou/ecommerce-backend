from fastapi import APIRouter
from typing import List
from Modules.Auth.CheckAuth import require_role
from Modules.Auth.Models import User
from Modules.Stock.Schemas import *
from Modules.Stock.Services.CategoryService import CategoryService, get_category_service
from Modules.Stock.Services.ProductService import ProductService, get_product_service
from Utils.Response import success_response
from fastapi import Depends
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/stock/admin", tags=["stock/admin"])

## Category Routes

@router.get("/categories")
def get_all_categories_controller(
    current_user: User = Depends(require_role(["admin"])),
    category_service: CategoryService = Depends(get_category_service),
    ) -> JSONResponse:
    categories = category_service.get_all_categories()
    
    return success_response(message="Categories fetched successfully", data=categories, status_code=200)


@router.get("/categories/{category_id}")
def get_category_by_id_controller(
    category_id: int,
    current_user: User = Depends(require_role(["admin"])),
    category_service: CategoryService = Depends(get_category_service),
    ) -> JSONResponse:
    category = category_service.get_category_by_id(category_id)
    return success_response(message="Category fetched successfully", data=category, status_code=200)

@router.post("/categories")
def create_category_controller(
    category_data: CreateCategorySchema,
    current_user: User = Depends(require_role(["admin"])),
    category_service: CategoryService = Depends(get_category_service),
    ) -> JSONResponse:
    print("Category data: ", category_data)
    return success_response(message="Category created successfully", data=category_data, status_code=201)

@router.put("/categories/{category_id}")
def update_category_controller(
    category_id: int,
    category_data: UpdateCategorySchema,
    current_user: User = Depends(require_role(["admin"])),
    category_service: CategoryService = Depends(get_category_service),
    ) -> JSONResponse:
    category = category_service.update_category(category_id, category_data)
    return success_response(message="Category updated successfully", data=category, status_code=200)


@router.delete("/categories/{category_id}")
def delete_category_controller(
    category_id: int,
    current_user: User = Depends(require_role(["admin"])),
    category_service: CategoryService = Depends(get_category_service),
    ) -> JSONResponse:
    category_service.delete_category(category_id)
    return success_response(message="Category deleted successfully", status_code=200)


## Product Routes

@router.get("/products")
def get_all_products_controller(
    current_user: User = Depends(require_role(["admin"])),
    product_service: ProductService = Depends(get_product_service),
    ) -> JSONResponse:
    products = product_service.get_all_products()
    return success_response(message="Products fetched successfully", data=products, status_code=200)


@router.get("/products/{product_id}")
def get_product_by_id_controller(
    product_id: int,
    current_user: User = Depends(require_role(["admin"])),
    product_service: ProductService = Depends(get_product_service),
    ) -> JSONResponse:
    product = product_service.get_product_by_id(product_id)
    return success_response(message="Product fetched successfully", data=product, status_code=200)


@router.post("/products")
def create_product_controller(
    product_data: CreateProductSchema,
    current_user: User = Depends(require_role(["admin"])),
    product_service: ProductService = Depends(get_product_service),
    ) -> JSONResponse:
    product = product_service.create_product(product_data)
    return success_response(message="Product created successfully", data=product, status_code=201)


@router.put("/products/{product_id}")
def update_product_controller(
    product_id: int,
    product_data: UpdateProductSchema,
    current_user: User = Depends(require_role(["admin"])),
    product_service: ProductService = Depends(get_product_service),
    ) -> JSONResponse:
    product = product_service.update_product(product_id, product_data)
    return success_response(message="Product updated successfully", data=product, status_code=200)

@router.delete("/products/{product_id}")
def delete_product_controller(
    product_id: int,
    current_user: User = Depends(require_role(["admin"])),
    product_service: ProductService = Depends(get_product_service),
    ) -> JSONResponse:
    product_service.delete_product(product_id)
    return success_response(message="Product deleted successfully", status_code=200)
