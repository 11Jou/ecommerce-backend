from abc import ABC, abstractmethod
from Modules.Order.Models import OrderItem
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from Core.Database import get_db


class IOrderItemsRepository(ABC):

    @abstractmethod
    def create_order_item(self, order_item: OrderItem) -> OrderItem:
        pass

    @abstractmethod
    def get_order_item_by_id(self, order_item_id: int) -> OrderItem:
        pass

    @abstractmethod
    def get_order_items_by_order_id(self, order_id: int) -> List[OrderItem]:
        pass

    @abstractmethod
    def get_all_order_items(self) -> List[OrderItem]:
        pass

    @abstractmethod
    def update_order_item(self, order_item: OrderItem) -> OrderItem:
        pass

    @abstractmethod
    def delete_order_item(self, order_item: OrderItem) -> None:
        pass


class OrderItemsRepository(IOrderItemsRepository):

    def __init__(self, db: Session):
        self.db = db

    def create_order_item(self, order_item: OrderItem) -> OrderItem:
        self.db.add(order_item)
        self.db.commit()
        self.db.refresh(order_item)
        return order_item
        
    def get_order_item_by_id(self, order_item_id: int) -> OrderItem:
        return self.db.query(OrderItem).filter(OrderItem.id == order_item_id).first()

    def get_order_items_by_order_id(self, order_id: int) -> List[OrderItem]:
        return self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

    def get_all_order_items(self) -> List[OrderItem]:
        return self.db.query(OrderItem).all()
        
    def update_order_item(self, order_item: OrderItem) -> OrderItem:
        self.db.commit()
        self.db.refresh(order_item)
        return order_item

    def delete_order_item(self, order_item: OrderItem) -> None:
        self.db.delete(order_item)
        self.db.commit()

def get_order_items_repository(db: Session = Depends(get_db)) -> IOrderItemsRepository:
    return OrderItemsRepository(db)