from abc import ABC, abstractmethod
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from Core.Database import get_db
from Modules.Order.Models import Order, OrderItem


class IOrderRepository(ABC):
    @abstractmethod
    def create_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_orders_by_user_id(self, user_id: int) -> List[Order]:
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

    @abstractmethod
    def create_order_items(self, order_items: List[OrderItem]) -> List[OrderItem]:
        pass

    @abstractmethod
    def stage_order_with_items(self, order: Order, order_items: List[OrderItem]) -> Order:
        pass

    @abstractmethod
    def get_order_item_by_id(self, order_item_id: int) -> OrderItem:
        pass

    @abstractmethod
    def get_all_order_items(self) -> List[OrderItem]:
        pass



class OrderRepository(IOrderRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_orders_by_user_id(self, user_id: int) -> List[Order]:
        return self.db.query(Order).filter(Order.user_id == user_id).all()

    def get_all_orders(self) -> List[Order]:
        return self.db.query(Order).all()

    def update_order(self, order: Order) -> Order:
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete_order(self, order: Order) -> None:
        self.db.delete(order)
        self.db.commit()

    def create_order_items(self, order_items: List[OrderItem]) -> List[OrderItem]:
        self.db.add_all(order_items)
        self.db.commit()
        for order_item in order_items:
            self.db.refresh(order_item)
        return order_items

    def stage_order_with_items(self, order: Order, order_items: List[OrderItem]) -> Order:
        self.db.add(order)
        self.db.flush()

        for order_item in order_items:
            order_item.order_id = order.id

        self.db.add_all(order_items)
        return order

    def get_order_item_by_id(self, order_item_id: int) -> OrderItem:
        return self.db.query(OrderItem).filter(OrderItem.id == order_item_id).first()

def get_order_repository(db: Session = Depends(get_db)) -> IOrderRepository:
    return OrderRepository(db)