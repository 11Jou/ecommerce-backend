from Modules.Stock.Repository.StockRepository import *
from Modules.Stock.Schemas import *
from Modules.Stock.Models import Stock
from fastapi import HTTPException
from Core.Database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


class StockService:

    def __init__(self, stock_repository: IStockRepository):
        self.stock_repository = stock_repository

    def get_stock_by_product_id(self, product_id: int) -> Stock:
        return self.stock_repository.get_stock_by_product_id(product_id)

    def create_stock(self, stock: Stock) -> Stock:
        new_stock = Stock(
            store_id=stock.store_id,
            product_id=stock.product_id,
            quantity=stock.quantity)
        return self.stock_repository.create_stock(new_stock)

    def update_stock(self, stock: Stock) -> Stock:
        existing_stock = self.get_stock_by_product_id(stock.product_id)
        if not existing_stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        update_data = stock.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(existing_stock, field, value)
        return self.stock_repository.update_stock(existing_stock)

    def delete_stock(self, stock_id: int) -> None:
        existing_stock = self.get_stock_by_product_id(stock_id)
        if not existing_stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        return self.stock_repository.delete_stock(existing_stock)

def get_stock_service(db: Session = Depends(get_db)) -> StockService:
    return StockService(get_stock_repository(db))