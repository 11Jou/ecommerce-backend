from abc import ABC, abstractmethod
from Modules.Stock.Models import Stock
from sqlalchemy.orm import Session
from fastapi import Depends
from Core.Database import get_db
from typing import List, Optional


class IStockRepository(ABC):

    @abstractmethod
    def get_all_stocks(self) -> List[Stock]:
        pass

    @abstractmethod
    def get_stocks_by_product_id(self, product_id: int) -> List[Stock]:
        pass

    @abstractmethod
    def get_stocks_by_store_id(self, store_id: int) -> List[Stock]:
        pass

    @abstractmethod
    def get_stock_by_product_id_and_store_id(self, product_id: int, store_id: int) -> Optional[Stock]:
        pass

    @abstractmethod
    def create_stock(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    def update_stock(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    def delete_stock(self, store_id: int, product_id: int) -> None:
        pass


class StockRepository(IStockRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all_stocks(self) -> List[Stock]:
        return self.db.query(Stock).all()

    def get_stocks_by_product_id(self, product_id: int) -> List[Stock]:
        return self.db.query(Stock).filter(Stock.product_id == product_id).all()

    def get_stocks_by_store_id(self, store_id: int) -> List[Stock]:
        return self.db.query(Stock).filter(Stock.store_id == store_id).all()

    def get_stock_by_product_id_and_store_id(self, product_id: int, store_id: int) -> Optional[Stock]:
        return (
            self.db.query(Stock)
            .filter(Stock.product_id == product_id, Stock.store_id == store_id)
            .first()
        )

    def create_stock(self, stock: Stock) -> Stock:
        self.db.add(stock)
        self.db.commit()
        self.db.refresh(stock)
        return stock

    def update_stock(self, stock: Stock) -> Stock:
        self.db.commit()
        self.db.refresh(stock)
        return stock

    def delete_stock(self, store_id: int, product_id: int) -> None:
        stock = self.get_stock_by_product_id_and_store_id(product_id, store_id)
        if stock:
            self.db.delete(stock)
            self.db.commit()


def get_stock_repository(db: Session = Depends(get_db)) -> IStockRepository:
    return StockRepository(db)
