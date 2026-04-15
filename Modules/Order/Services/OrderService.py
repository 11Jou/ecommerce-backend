from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from Core.Database import get_db
from Modules.Order.Mappers.OrderItemMapper import to_order_item_dict
from Modules.Order.Mappers.OrderMapper import to_order_dict
from Modules.Order.Models import CartItem, Order, OrderItem
from Modules.Order.Repository.OrderRepository import IOrderRepository, get_order_repository


class OrderService:
    def __init__(self, order_repository: IOrderRepository):
        self.order_repository = order_repository

    def create_order(self, order: Order) -> Order:
        return self.order_repository.create_order(order)

    def get_order_by_id(self, order_id: int) -> Order:
        existing_order = self.order_repository.get_order_by_id(order_id)
        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return to_order_dict(existing_order)

    def get_all_orders(self) -> List[Order]:
        orders = self.order_repository.get_all_orders()
        return [to_order_dict(order) for order in orders]

    def get_all_orders_by_user_id(self, user_id: int) -> List[Order]:
        orders = self.order_repository.get_all_orders_by_user_id(user_id)
        return orders

    def update_order(self, order: Order) -> Order:
        existing_order = self.order_repository.get_order_by_id(order.id)
        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")
        updated_order = self.order_repository.update_order(order)
        return to_order_dict(updated_order)

    def delete_order(self, order_id: int) -> None:
        existing_order = self.order_repository.get_order_by_id(order_id)
        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")
        self.order_repository.delete_order(existing_order)

    def create_order_items(self, cart_items: List[CartItem], order_id: int) -> List[OrderItem]:
        order_items = []
        for item in cart_items:
            new_order_item = OrderItem(
                order_id=order_id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            order_items.append(new_order_item)
        return self.order_repository.create_order_items(order_items)

    def get_order_item_by_id(self, order_item_id: int) -> OrderItem:
        existing_order_item = self.order_repository.get_order_item_by_id(order_item_id)
        if not existing_order_item:
            raise HTTPException(status_code=404, detail="Order item not found")
        return existing_order_item

    def get_order_items_by_order_id(self, order_id: int) -> List[OrderItem]:
        order_items = self.order_repository.get_order_items_by_order_id(order_id)
        return order_items


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(get_order_repository(db))