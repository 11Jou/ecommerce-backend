from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Database.AsyncDatabase import get_db
from Modules.Stock.Models import Category
from Modules.Stock.Repository.CategoryRepository import (
    ICategoryRepository,
    get_category_repository,
)
from Modules.Stock.Schemas import CreateCategorySchema, UpdateCategorySchema


class CategoryService:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    async def get_all_categories(self) -> List[Category]:
        return await self.category_repository.get_all_categories()

    async def get_category_by_id(self, category_id: int) -> Category:
        existing_category = await self.category_repository.get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")
        return existing_category

    async def create_category(self, category: CreateCategorySchema) -> Category:
        new_category = Category(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
        return await self.category_repository.create_category(new_category)

    async def update_category(self, category_id: int, category: UpdateCategorySchema) -> Category:
        existing_category = await self.category_repository.get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")

        update_data = category.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(existing_category, field, value)

        return await self.category_repository.update_category(existing_category)

    async def delete_category(self, category_id: int) -> None:
        existing_category = await self.category_repository.get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")

        await self.category_repository.delete_category(category_id)


def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    return CategoryService(category_repository=get_category_repository(db))
