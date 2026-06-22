from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Modules.Auth.CheckAuth import require_role
from Modules.Auth.Models import User
from Modules.Stock.Mappers.CategoryMapper import to_category_dict
from Modules.Stock.Schemas import CreateCategorySchema, UpdateCategorySchema
from Modules.Stock.Services.CategoryService import CategoryService, get_category_service
from Utils.Response import success_response

router = APIRouter(prefix="/admin/stock/categories", tags=["admin/stock/categories"])


@router.get("/")
async def get_all_categories_controller(
    current_user: User = Depends(require_role(["admin"])),
    category_service: CategoryService = Depends(get_category_service),
) -> JSONResponse:
    categories = await category_service.get_all_categories()
    return success_response(
        message="Categories fetched successfully",
        data=[to_category_dict(category) for category in categories],
        status_code=200,
    )


@router.get("/{category_id}")
async def get_category_by_id_controller(
    category_id: int,
    current_user: User = Depends(require_role(["admin"])),
    category_service: CategoryService = Depends(get_category_service),
) -> JSONResponse:
    category = await category_service.get_category_by_id(category_id)
    return success_response(
        message="Category fetched successfully",
        data=to_category_dict(category),
        status_code=200,
    )


@router.post("/")
async def create_category_controller(
    category_data: CreateCategorySchema,
    current_user: User = Depends(require_role(["admin"])),
    category_service: CategoryService = Depends(get_category_service),
) -> JSONResponse:
    category = await category_service.create_category(category_data)
    return success_response(
        message="Category created successfully",
        data=to_category_dict(category),
        status_code=201,
    )


@router.put("/{category_id}")
async def update_category_controller(
    category_id: int,
    category_data: UpdateCategorySchema,
    current_user: User = Depends(require_role(["admin"])),
    category_service: CategoryService = Depends(get_category_service),
) -> JSONResponse:
    category = await category_service.update_category(category_id, category_data)
    return success_response(
        message="Category updated successfully",
        data=to_category_dict(category),
        status_code=200,
    )


@router.delete("/{category_id}")
async def delete_category_controller(
    category_id: int,
    current_user: User = Depends(require_role(["admin"])),
    category_service: CategoryService = Depends(get_category_service),
) -> JSONResponse:
    await category_service.delete_category(category_id)
    return success_response(
        message="Category deleted successfully",
        status_code=200,
    )
