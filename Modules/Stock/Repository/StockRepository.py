from abc import ABC, abstractmethod
from Modules.Stock.Models import Stock
from sqlalchemy.orm import Session
from fastapi import Depends
from Core.Database import get_db

class IStockRepository(ABC):
    @abstractmethod
    def get_stock_by_product_id(self, product_id: int) -> Stock:
        pass

    @abstractmethod
    def create_stock(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    def update_stock(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    def delete_stock(self, stock_id: int) -> None:
        pass

class StockRepository(IStockRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_stock_by_product_id(self, product_id: int) -> Stock:
        return self.db.query(Stock).filter(Stock.product_id == product_id).first()

    def create_stock(self, stock: Stock) -> Stock:
        self.db.add(stock)
        self.db.commit()
        self.db.refresh(stock)
        return stock
        
    def update_stock(self, stock: Stock) -> Stock:
        self.db.commit()
        self.db.refresh(stock)
        return stock

    def delete_stock(self, stock_id: int) -> None:
        stock = self.get_stock_by_product_id(stock_id)
        if stock:
            self.db.delete(stock)
            self.db.commit()
            return True
        return False

def get_stock_repository(db: Session = Depends(get_db)) -> IStockRepository:
    return StockRepository(db)