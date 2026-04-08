from typing import List

from Modules.Stock.Repository.StockRepository import IStockRepository, get_stock_repository
from Modules.Stock.Schemas import CreateStockSchema, StockSchema, UpdateStockSchema
from Modules.Stock.Models import Stock
from fastapi import HTTPException
from Core.Database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


class StockService:

    def __init__(self, stock_repository: IStockRepository):
        self.stock_repository = stock_repository

    def _serialize_stock(self, stock: Stock) -> dict:
        return StockSchema(
            store_id=stock.store_id,
            product_id=stock.product_id,
            quantity=stock.quantity,
            created_at=stock.created_at,
            updated_at=stock.updated_at,
        ).model_dump(mode="json")

    def get_all_stocks(self) -> List[dict]:
        stocks = self.stock_repository.get_all_stocks()
        return [self._serialize_stock(stock) for stock in stocks]

    def get_stocks_by_product_id(self, product_id: int) -> List[dict]:
        stocks = self.stock_repository.get_stocks_by_product_id(product_id)
        return [self._serialize_stock(stock) for stock in stocks]

    def get_stocks_by_store_id(self, store_id: int) -> List[dict]:
        stocks = self.stock_repository.get_stocks_by_store_id(store_id)
        return [self._serialize_stock(stock) for stock in stocks]

    def get_stock_by_product_id_and_store_id(self, product_id: int, store_id: int) -> dict:
        stock = self.stock_repository.get_stock_by_product_id_and_store_id(product_id, store_id)
        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        return self._serialize_stock(stock)

    def create_stock(self, data: CreateStockSchema) -> dict:
        existing = self.stock_repository.get_stock_by_product_id_and_store_id(data.product_id, data.store_id)
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
        created_stock = self.stock_repository.create_stock(new_stock)
        return self._serialize_stock(created_stock)

    def update_stock(self, store_id: int, product_id: int, data: UpdateStockSchema) -> dict:
        existing = self.stock_repository.get_stock_by_product_id_and_store_id(product_id, store_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Stock not found")
        existing.quantity = data.quantity
        updated_stock = self.stock_repository.update_stock(existing)
        return self._serialize_stock(updated_stock)

    def delete_stock(self, store_id: int, product_id: int) -> None:
        existing = self.stock_repository.get_stock_by_product_id_and_store_id(product_id, store_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Stock not found")
        self.stock_repository.delete_stock(store_id, product_id)


def get_stock_service(db: Session = Depends(get_db)) -> StockService:
    return StockService(get_stock_repository(db))
