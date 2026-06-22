from abc import ABC, abstractmethod
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from Core.Database.AsyncDatabase import get_db
from Modules.Stock.Models import Product, Stock


class IProductRepository(ABC):
    @abstractmethod
    async def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    async def get_product_by_id(self, product_id: int) -> Product:
        pass

    async def get_product_by_category(self, category_id: int) -> List[Product]:
        pass

    @abstractmethod
    async def create_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def update_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def delete_product(self, product_id: int) -> None:
        pass


class ProductRepository(IProductRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_products(self) -> List[Product]:
        result = await self.db.execute(
            select(Product).options(joinedload(Product.category))
        )
        return list(result.unique().scalars().all())

    async def get_active_products(self, name: Optional[str] = None) -> List[Product]:
        stmt = (
            select(Product)
            .options(
                joinedload(Product.category),
                joinedload(Product.stocks).joinedload(Stock.store),
            )
            .where(Product.is_active == True)
        )

        if name and name.strip():
            stmt = stmt.where(Product.name.ilike(f"%{name.strip()}%"))

        result = await self.db.execute(stmt)
        return list(result.unique().scalars().all())

    async def get_product_by_id(self, product_id: int) -> Product:
        result = await self.db.execute(
            select(Product)
            .options(
                joinedload(Product.category),
                joinedload(Product.stocks).joinedload(Stock.store),
            )
            .where(Product.id == product_id)
        )
        return result.unique().scalars().first()

    async def get_product_by_category(self, category_id: int) -> List[Product]:
        result = await self.db.execute(
            select(Product)
            .options(
                joinedload(Product.category),
                joinedload(Product.stocks).joinedload(Stock.store),
            )
            .where(Product.category_id == category_id)
        )
        return list(result.unique().scalars().all())

    async def create_product(self, product: Product) -> Product:
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def update_product(self, product: Product) -> Product:
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete_product(self, product: Product) -> None:
        await self.db.delete(product)
        await self.db.commit()


def get_product_repository(db: AsyncSession = Depends(get_db)) -> IProductRepository:
    return ProductRepository(db)
