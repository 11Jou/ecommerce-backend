from Modules.Stock.Services.CategoryService import CategoryService, get_category_service
from Modules.Stock.Schemas import CategorySchema
from fastapi import Depends
from Modules.Auth.CheckAuth import get_current_user
from Modules.Auth.Models import User
from typing import List
from fastapi import APIRouter


router = APIRouter(prefix="/stock", tags=["stock"])

@router.get("/categories", response_model=List[CategorySchema])
def get_all_categories_controller(
    current_user: User = Depends(get_current_user),
    category_service: CategoryService = Depends(get_category_service)
    ) -> List[CategorySchema]:
    return category_service.get_all_categories()