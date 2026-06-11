from abc import ABC, abstractmethod
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

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
    def get_order_by_id(self, order_id: int, user_id: int) -> Order:
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
    def add_order_items(self, order_items: List[OrderItem]) -> List[OrderItem]:
        pass

    @abstractmethod
    def get_order_item_by_id(self, order_item_id: int) -> OrderItem:
        pass



class OrderRepository(IOrderRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.flush()
        return order

    def get_orders_by_user_id(self, user_id: int) -> List[Order]:
        items_loader = joinedload(Order.items)
        product_loader = items_loader.joinedload(OrderItem.product)
        store_loader = items_loader.joinedload(OrderItem.store)
        address_loader = joinedload(Order.address)
        user_loader = joinedload(Order.user)

        return (
            self.db.query(Order)
            .options(
                items_loader,
                product_loader,
                store_loader,
                address_loader,
                user_loader,
            )
            .filter(Order.user_id == user_id)
            .all()
        )

    def get_order_by_id(self, order_id: int, user_id: int) -> Order | None:
        items_loader = joinedload(Order.items)
        product_loader = items_loader.joinedload(OrderItem.product)
        store_loader = items_loader.joinedload(OrderItem.store)
        address_loader = joinedload(Order.address)
        user_loader = joinedload(Order.user)
        return (
            self.db.query(Order)
            .options(items_loader, product_loader, store_loader, address_loader, user_loader)
            .filter(Order.id == order_id, Order.user_id == user_id)
            .first()
        )

    def get_all_orders(self) -> List[Order]:
        return self.db.query(Order).all()

    def update_order(self, order: Order) -> Order:
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete_order(self, order: Order) -> None:
        self.db.delete(order)
        self.db.commit()

    def add_order_items(self, order_items: List[OrderItem]) -> List[OrderItem]:
        self.db.add_all(order_items)
        return order_items

    def get_order_item_by_id(self, order_item_id: int) -> OrderItem:
        return self.db.query(OrderItem).filter(OrderItem.id == order_item_id).first()

def get_order_repository(db: Session = Depends(get_db)) -> IOrderRepository:
    return OrderRepository(db)