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

    def _serialize_category(self, category: Category) -> dict:
        return CategorySchema(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at,
            updated_at=category.updated_at,
        ).model_dump(mode="json")

    def get_all_categories(self) -> List[dict]:
        categories = self.category_repository.get_all_categories()
        return [self._serialize_category(category) for category in categories]

    def get_category_by_id(self, category_id: int) -> dict:
        existing_category = self.category_repository.get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")
        return self._serialize_category(existing_category)

    def create_category(self, category: CreateCategorySchema) -> dict:
        new_category = Category(name=category.name, description=category.description , is_active=category.is_active)
        created_category = self.category_repository.create_category(new_category)
        return self._serialize_category(created_category)

    def update_category(self, category_id: int, category: UpdateCategorySchema) -> dict:
        existing_category = self.category_repository.get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")

        update_data = category.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(existing_category, field, value)

        updated_category = self.category_repository.update_category(existing_category)
        return self._serialize_category(updated_category)

    def delete_category(self, category_id: int) -> None:
        existing_category = self.category_repository.get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")

        self.category_repository.delete_category(category_id)


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(category_repository=get_category_repository(db))