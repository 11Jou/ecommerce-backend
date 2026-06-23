from abc import ABC, abstractmethod
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Database.AsyncDatabase import get_db
from Modules.Stock.Models import Stock
from Utils.Pagination import PaginatedResult, count_total, paginate


class IStockRepository(ABC):
    @abstractmethod
    async def get_all_stocks(self, page: int, page_size: int) -> PaginatedResult[Stock]:
        pass

    @abstractmethod
    async def get_stocks_by_product_id(
        self, product_id: int, page: int, page_size: int
    ) -> PaginatedResult[Stock]:
        pass

    @abstractmethod
    async def get_stocks_by_store_id(
        self, store_id: int, page: int, page_size: int
    ) -> PaginatedResult[Stock]:
        pass

    @abstractmethod
    async def get_stock_by_product_id_and_store_id(
        self, product_id: int, store_id: int
    ) -> Optional[Stock]:
        pass

    @abstractmethod
    async def create_stock(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    async def update_stock(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    async def delete_stock(self, store_id: int, product_id: int) -> None:
        pass


class StockRepository(IStockRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_stocks(self, page: int, page_size: int) -> PaginatedResult[Stock]:
        stmt = select(Stock)
        total = await count_total(self.db, stmt)
        result = await self.db.execute(paginate(stmt, page, page_size))
        items = list(result.scalars().all())
        return PaginatedResult(items=items, total=total)

    async def get_stocks_by_product_id(
        self, product_id: int, page: int, page_size: int
    ) -> PaginatedResult[Stock]:
        stmt = select(Stock).where(Stock.product_id == product_id)
        total = await count_total(self.db, stmt)
        result = await self.db.execute(paginate(stmt, page, page_size))
        items = list(result.scalars().all())
        return PaginatedResult(items=items, total=total)

    async def get_stocks_by_store_id(
        self, store_id: int, page: int, page_size: int
    ) -> PaginatedResult[Stock]:
        stmt = select(Stock).where(Stock.store_id == store_id)
        total = await count_total(self.db, stmt)
        result = await self.db.execute(paginate(stmt, page, page_size))
        items = list(result.scalars().all())
        return PaginatedResult(items=items, total=total)

    async def get_stock_by_product_id_and_store_id(
        self, product_id: int, store_id: int
    ) -> Optional[Stock]:
        result = await self.db.execute(
            select(Stock).where(Stock.product_id == product_id, Stock.store_id == store_id)
        )
        return result.scalars().first()

    async def create_stock(self, stock: Stock) -> Stock:
        self.db.add(stock)
        await self.db.commit()
        await self.db.refresh(stock)
        return stock

    async def update_stock(self, stock: Stock) -> Stock:
        await self.db.commit()
        await self.db.refresh(stock)
        return stock

    async def delete_stock(self, store_id: int, product_id: int) -> None:
        stock = await self.get_stock_by_product_id_and_store_id(product_id, store_id)
        if stock:
            await self.db.delete(stock)
            await self.db.commit()


def get_stock_repository(db: AsyncSession = Depends(get_db)) -> IStockRepository:
    return StockRepository(db)
