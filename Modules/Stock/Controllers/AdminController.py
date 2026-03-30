from fastapi import APIRouter
from typing import List
from Modules.Auth.CheckAuth import require_role
from Modules.Auth.Models import User
from Modules.Stock.Schemas import CategorySchema, CreateCategorySchema
from Modules.Stock.Services.CategoryService import CategoryService, get_category_service
from fastapi import Depends

router = APIRouter(prefix="/stock/admin", tags=["stock/admin"])

@router.post("/categories", response_model=CategorySchema)
def create_category_controller(
    category_data: CreateCategorySchema,
    current_user: User = Depends(require_role(["admin"])),
    category_service: CategoryService = Depends(get_category_service),
    ) -> CategorySchema:
    return category_service.create_category(category_data)