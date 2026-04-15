from Modules.Order.Services.OrderService import OrderService, get_order_service
from Modules.Order.Models import Order, OrderItem, OrderStatus
from Modules.User.Models import User
from fastapi import HTTPException
from Core.Database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List

class CheckoutService:

    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    def makeOrder(self, current_user: User) -> Order:
        new_order = Order(
            user_id=current_user.id,
            status=OrderStatus.PENDING
        )
        created_order = self.order_service.order_repository.create_order(new_order)

        existing_cart = self.cart_service.get_cart_by_user_id(current_user.id)
        if not existing_cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        new_order_items = self.order_service.create_order_items(existing_cart.items, created_order.id)
        return created_order

def get_checkout_service(db: Session = Depends(get_db)) -> CheckoutService:
    return CheckoutService(get_order_service(db))