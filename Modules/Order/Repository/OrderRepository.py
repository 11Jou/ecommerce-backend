from abc import ABC, abstractmethod
from Modules.Order.Models import Order
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from Core.Database import get_db


class IOrderRepository(ABC):

    @abstractmethod
    def create_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: int) -> Order:
        pass

    @abstractmethod
    def get_all_orders(self) -> List[Order]:
        pass

    @abstractmethod
    def update_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    def delete_order(self, order: Order) -> None:
        pass


class OrderRepository(IOrderRepository):

    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order_by_id(self, order_id: int) -> Order:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_all_orders(self) -> List[Order]:
        return self.db.query(Order).all()

    def update_order(self, order: Order) -> Order:
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete_order(self, order: Order) -> None:
        self.db.delete(order)
        self.db.commit()


def get_order_repository(db: Session = Depends(get_db)) -> IOrderRepository:
    return OrderRepository(db)