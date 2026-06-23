from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from Modules.Stock.Mappers.CategoryMapper import to_category_dict
from Modules.Stock.Mappers.ProductMapper import to_product_with_availability_dict
from Modules.Stock.Schemas import CategorySchema, ProductSchema
from Modules.Stock.Services.CategoryService import CategoryService, get_category_service
from Modules.Stock.Services.ProductService import ProductService, get_product_service
from Utils.Pagination import PaginationParams, build_pagination_meta
from Utils.Response import success_response

router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/categories")
async def get_all_categories_controller(
    category_service: CategoryService = Depends(get_category_service),
    pagination: PaginationParams = Depends(),
) -> JSONResponse:
    result = await category_service.get_all_categories(pagination.page, pagination.page_size)
    return success_response(
        message="Categories fetched successfully",
        data=[to_category_dict(category) for category in result.items],
        pagination=build_pagination_meta(pagination.page, pagination.page_size, result.total),
        status_code=200,
    )


@router.get("/categories/{category_id}")
async def get_category_by_id_controller(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
) -> JSONResponse:
    category = await category_service.get_category_by_id(category_id)
    return success_response(
        message="Category fetched successfully",
        data=to_category_dict(category),
        status_code=200,
    )


@router.get("/products")
async def get_all_products_controller(
    name: Optional[str] = Query(None),
    product_service: ProductService = Depends(get_product_service),
    pagination: PaginationParams = Depends(),
) -> JSONResponse:
    result = await product_service.get_active_products_with_availability(
        name=name, page=pagination.page, page_size=pagination.page_size
    )
    return success_response(
        message="Products fetched successfully",
        data=[to_product_with_availability_dict(product) for product in result.items],
        pagination=build_pagination_meta(pagination.page, pagination.page_size, result.total),
        status_code=200,
    )


@router.get("/products/{product_id}")
async def get_product_by_id_controller(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
) -> JSONResponse:
    product = await product_service.get_product_by_id_with_availability(product_id)
    return success_response(
        message="Product fetched successfully",
        data=to_product_with_availability_dict(product),
        status_code=200,
    )
