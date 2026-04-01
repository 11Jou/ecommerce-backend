from Modules.Stock.Repository.CategoryRepository import CategoryRepository, ICategoryRepository, get_category_repository
from Modules.Stock.Models import Category
from Modules.Stock.Schemas import *
from fastapi import HTTPException
from typing import List
from Core.Database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


class CategoryService:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def get_all_categories(self) -> List[Category]:
        return self.category_repository.get_all_categories()

    def get_category_by_id(self, category_id: int) -> Category:
        existing_category = self.category_repository.get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")
        return existing_category

    def create_category(self, category: CreateCategorySchema) -> Category:
        new_category = Category(name=category.name, description=category.description , is_active=category.is_active)
        return self.category_repository.create_category(new_category)

    def update_category(self, category_id: int, category: UpdateCategorySchema) -> Category:
        existing_category = self.get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")

        update_data = category.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(existing_category, field, value)

        return self.category_repository.update_category(existing_category)

    def delete_category(self, category_id: int) -> None:
        existing_category = self.get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")

        return self.category_repository.delete_category(existing_category)


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(category_repository=get_category_repository(db))