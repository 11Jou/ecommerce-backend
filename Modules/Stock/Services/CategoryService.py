from Modules.Stock.Repository.CategoryRepository import CategoryRepository, ICategoryRepository, get_category_repository
from Modules.Stock.Models import Category
from Modules.Stock.Schemas import *
from Modules.Stock.Mappers.CategoryMapper import to_category_dict
from fastapi import HTTPException
from typing import List
from Core.Database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


class CategoryService:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def get_all_categories(self) -> List[dict]:
        categories = self.category_repository.get_all_categories()
        return [to_category_dict(category) for category in categories]

    def get_category_by_id(self, category_id: int) -> dict:
        existing_category = self.category_repository.get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")
        return to_category_dict(existing_category)

    def create_category(self, category: CreateCategorySchema) -> dict:
        new_category = Category(name=category.name, description=category.description , is_active=category.is_active)
        created_category = self.category_repository.create_category(new_category)
        return to_category_dict(created_category)

    def update_category(self, category_id: int, category: UpdateCategorySchema) -> dict:
        existing_category = self.category_repository.get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")

        update_data = category.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(existing_category, field, value)

        updated_category = self.category_repository.update_category(existing_category)
        return to_category_dict(updated_category)

    def delete_category(self, category_id: int) -> None:
        existing_category = self.category_repository.get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")

        self.category_repository.delete_category(category_id)


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(category_repository=get_category_repository(db))