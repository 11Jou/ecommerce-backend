from typing import List

from Modules.Stock.Repository.StockRepository import IStockRepository, get_stock_repository
from Modules.Stock.Schemas import CreateStockSchema, UpdateStockSchema
from Modules.Stock.Models import Stock
from fastapi import HTTPException
from Core.Database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


class StockService:

    def __init__(self, stock_repository: IStockRepository):
        self.stock_repository = stock_repository

    def get_all_stocks(self) -> List[Stock]:
        return self.stock_repository.get_all_stocks()

    def get_stocks_by_product_id(self, product_id: int) -> List[Stock]:
        return self.stock_repository.get_stocks_by_product_id(product_id)

    def get_stocks_by_store_id(self, store_id: int) -> List[Stock]:
        return self.stock_repository.get_stocks_by_store_id(store_id)

    def get_stock_by_product_id_and_store_id(self, product_id: int, store_id: int) -> Stock:
        stock = self.stock_repository.get_stock_by_product_id_and_store_id(product_id, store_id)
        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        return stock

    def create_stock(self, data: CreateStockSchema) -> Stock:
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
        return self.stock_repository.create_stock(new_stock)

    def update_stock(self, store_id: int, product_id: int, data: UpdateStockSchema) -> Stock:
        existing = self.stock_repository.get_stock_by_product_id_and_store_id(product_id, store_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Stock not found")
        existing.quantity = data.quantity
        return self.stock_repository.update_stock(existing)

    def delete_stock(self, store_id: int, product_id: int) -> None:
        existing = self.stock_repository.get_stock_by_product_id_and_store_id(product_id, store_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Stock not found")
        self.stock_repository.delete_stock(store_id, product_id)


def get_stock_service(db: Session = Depends(get_db)) -> StockService:
    return StockService(get_stock_repository(db))
