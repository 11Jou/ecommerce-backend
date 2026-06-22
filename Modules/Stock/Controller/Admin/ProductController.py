from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Modules.Auth.CheckAuth import require_role
from Modules.Auth.Models import User
from Modules.Stock.Mappers.ProductMapper import to_product_dict
from Modules.Stock.Schemas import CreateProductSchema, UpdateProductSchema
from Modules.Stock.Services.ProductService import ProductService, get_product_service
from Utils.Response import success_response

router = APIRouter(tags=["stock/admin/products"])


@router.get("/products")
async def get_all_products_controller(
    current_user: User = Depends(require_role(["admin"])),
    product_service: ProductService = Depends(get_product_service),
) -> JSONResponse:
    products = await product_service.get_all_products()
    return success_response(
        message="Products fetched successfully",
        data=[to_product_dict(product) for product in products],
        status_code=200,
    )


@router.get("/products/{product_id}")
async def get_product_by_id_controller(
    product_id: int,
    current_user: User = Depends(require_role(["admin"])),
    product_service: ProductService = Depends(get_product_service),
) -> JSONResponse:
    product = await product_service.get_product_by_id(product_id)
    return success_response(
        message="Products fetched successfully",
        data=to_product_dict(product),
        status_code=200,
    )


@router.post("/products")
async def create_product_controller(
    product_data: CreateProductSchema,
    current_user: User = Depends(require_role(["admin"])),
    product_service: ProductService = Depends(get_product_service),
) -> JSONResponse:
    product = await product_service.create_product(product_data)
    return success_response(
        message="Product created successfully",
        data=to_product_dict(product),
        status_code=201,
    )


@router.put("/products/{product_id}")
async def update_product_controller(
    product_id: int,
    product_data: UpdateProductSchema,
    current_user: User = Depends(require_role(["admin"])),
    product_service: ProductService = Depends(get_product_service),
) -> JSONResponse:
    product = await product_service.update_product(product_id, product_data)
    return success_response(
        message="Product updated successfully",
        data=to_product_dict(product),
        status_code=200,
    )


@router.delete("/products/{product_id}")
async def delete_product_controller(
    product_id: int,
    current_user: User = Depends(require_role(["admin"])),
    product_service: ProductService = Depends(get_product_service),
) -> JSONResponse:
    await product_service.delete_product(product_id)
    return success_response(message="Product deleted successfully", status_code=200)
