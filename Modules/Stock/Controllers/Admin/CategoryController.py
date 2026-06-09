from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Modules.Auth.CheckAuth import require_role
from Modules.Auth.Models import User
from Modules.Stock.Schemas import CreateCategorySchema, UpdateCategorySchema
from Modules.Stock.Services.CategoryService import CategoryService, get_category_service
from Utils.Response import success_response

router = APIRouter(tags=["stock/admin/categories"])




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
    category = category_service.create_category(category_data)
    return success_response(message="Category created successfully", data=category, status_code=201)


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
