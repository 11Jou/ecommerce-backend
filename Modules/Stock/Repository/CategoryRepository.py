from abc import ABC, abstractmethod
from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Database import get_db
from Modules.Stock.Models import Category


class ICategoryRepository(ABC):
    @abstractmethod
    async def get_all_categories(self) -> List[Category]:
        pass

    @abstractmethod
    async def get_category_by_id(self, category_id: int) -> Category:
        pass

    @abstractmethod
    async def create_category(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def update_category(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def delete_category(self, category_id: int) -> None:
        pass


class CategoryRepository(ICategoryRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_categories(self) -> List[Category]:
        result = await self.db.execute(select(Category))
        return list(result.scalars().all())

    async def get_category_by_id(self, category_id: int) -> Category:
        result = await self.db.execute(select(Category).where(Category.id == category_id))
        return result.scalars().first()

    async def create_category(self, category: Category) -> Category:
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def update_category(self, category: Category) -> Category:
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete_category(self, category_id: int) -> None:
        category = await self.get_category_by_id(category_id)
        if category:
            await self.db.delete(category)
            await self.db.commit()


def get_category_repository(db: AsyncSession = Depends(get_db)) -> ICategoryRepository:
    return CategoryRepository(db)
