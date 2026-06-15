from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from Core.Database import get_db
from Modules.Adresses.Services import AdressesService, get_adresses_service
from Modules.Order.Models import Cart, CartItem, Order, OrderItem, OrderStatus
from Modules.Order.Repository.OrderRepository import IOrderRepository, get_order_repository
from Modules.Order.Schemas import CreateOrderSchema
from Modules.Order.Services.CartService import CartService, get_cart_service


class OrderService:
    def __init__(
        self,
        db: Session,
        order_repository: IOrderRepository,
        cart_service: CartService,
        adresses_service: AdressesService,):

        self.db = db
        self.order_repository = order_repository
        self.cart_service = cart_service
        self.adresses_service = adresses_service


    def _build_order_items_from_cart(self, cart_items: List[CartItem]) -> List[OrderItem]:
        return [
            OrderItem(
                product_id=cart_item.product.id,
                store_id=cart_item.store.id,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price,
                total_price=cart_item.total_price,)
            for cart_item in cart_items]



    def place_order(self, user_id: int, order_data: CreateOrderSchema) -> Order:

        cart = self.cart_service.get_cart_by_user_id(user_id)
        address = self.adresses_service.get_address_by_id(user_id, order_data.address_id)


        self.adresses_service.validate_user_address(user_id, address)
        self.cart_service.validate_cart(cart)

        order = Order(user_id=user_id, status=OrderStatus.PENDING_PAYMENT, address_id=address.id, total_amount=cart.total_price)

        order_items = self._build_order_items_from_cart(cart.items)

        try:
            new_order = self.order_repository.create_order(order)
            self.order_repository.add_order_items(order_items)
            self.cart_service.clear_cart_without_commit(cart.id)
            self.db.commit()
            self.db.refresh(new_order)

        except Exception:
            self.db.rollback()
            raise

        return new_order


    def get_orders_by_user_id(self, user_id: int) -> List[Order]:
        return self.order_repository.get_orders_by_user_id(user_id)


    def get_order_by_id(self, order_id: int, user_id: int) -> Order:
        order = self.order_repository.get_order_by_id(order_id, user_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order



def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(
        db=db,
        order_repository=get_order_repository(db),
        cart_service=get_cart_service(db),
        adresses_service=get_adresses_service(db),
    )


