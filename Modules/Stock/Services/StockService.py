from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Database.AsyncDatabase import get_db
from Modules.Stock.Models import Stock
from Modules.Stock.Repository.StockRepository import IStockRepository, get_stock_repository
from Modules.Stock.Schemas import CreateStockSchema, UpdateStockSchema


class StockService:
    def __init__(self, stock_repository: IStockRepository):
        self.stock_repository = stock_repository

    async def get_all_stocks(self) -> List[Stock]:
        return await self.stock_repository.get_all_stocks()

    async def get_stocks_by_product_id(self, product_id: int) -> List[Stock]:
        return await self.stock_repository.get_stocks_by_product_id(product_id)

    async def get_stocks_by_store_id(self, store_id: int) -> List[Stock]:
        return await self.stock_repository.get_stocks_by_store_id(store_id)

    async def check_stock_availability(self, product_id: int, store_id: int, quantity: int) -> bool:
        stock = await self.stock_repository.get_stock_by_product_id_and_store_id(product_id, store_id)
        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        if stock.quantity < quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        return True

    async def reserve_stock(self, product_id: int, store_id: int, quantity: int) -> Stock:
        stock = await self.stock_repository.get_stock_by_product_id_and_store_id(product_id, store_id)
        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        if stock.quantity < quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        stock.quantity -= quantity
        return stock

    async def release_stock(self, product_id: int, store_id: int, quantity: int) -> Stock:
        stock = await self.stock_repository.get_stock_by_product_id_and_store_id(product_id, store_id)
        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        stock.quantity += quantity
        return stock

    async def get_stock_by_product_id_and_store_id(self, product_id: int, store_id: int) -> Stock:
        stock = await self.stock_repository.get_stock_by_product_id_and_store_id(product_id, store_id)
        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        return stock

    async def create_stock(self, data: CreateStockSchema) -> Stock:
        existing = await self.stock_repository.get_stock_by_product_id_and_store_id(
            data.product_id, data.store_id
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Stock already exists for this store and product; use update instead",
            )
        new_stock = Stock(
            store_id=data.store_id,
            product_id=data.product_id,
            quantity=data.quantity,
        )
        return await self.stock_repository.create_stock(new_stock)

    async def update_stock(self, store_id: int, product_id: int, data: UpdateStockSchema) -> Stock:
        existing = await self.stock_repository.get_stock_by_product_id_and_store_id(product_id, store_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Stock not found")
        existing.quantity = data.quantity
        return await self.stock_repository.update_stock(existing)

    async def delete_stock(self, store_id: int, product_id: int) -> None:
        existing = await self.stock_repository.get_stock_by_product_id_and_store_id(product_id, store_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Stock not found")
        await self.stock_repository.delete_stock(store_id, product_id)


def get_stock_service(db: AsyncSession = Depends(get_db)) -> StockService:
    return StockService(get_stock_repository(db))
