from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from Core.Database import get_db
from Modules.Order.Models import Cart, CartItem, Order, OrderItem, OrderStatus
from Modules.Order.Repository.CartRepository import ICartRepository, get_cart_repository
from Modules.Order.Repository.OrderRepository import IOrderRepository, get_order_repository
from Modules.Order.Schemas import CreateOrderSchema
from Modules.Order.Services.CartService import CartService, get_cart_service
from Modules.Stock.Services.ProductService import ProductService, get_product_service
from Modules.Stock.Services.StockService import StockService, get_stock_service


class OrderService:
    def __init__(
        self,
        db: Session,
        order_repository: IOrderRepository,
        cart_repository: ICartRepository,
        cart_service: CartService,
        product_service: ProductService,
        stock_service: StockService,
    ):
        self.db = db
        self.order_repository = order_repository
        self.cart_repository = cart_repository
        self.cart_service = cart_service
        self.product_service = product_service
        self.stock_service = stock_service

    def validate_cart(self, cart: Cart) -> None:
        if not cart or not cart.items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        for item in cart.items:
            if item.quantity <= 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Quantity must be greater than 0 for product {item.product_id}",
                )

            if not item.product.is_active:
                raise HTTPException(
                    status_code=400,
                    detail=f"Product {item.product.name} is not active",
                )

            self.stock_service.check_stock_availability(
                item.product.id,
                item.store_id,
                item.quantity,
            )

    def compute_item_total_price(self, unit_price, quantity: int) -> float:
        return round(float(unit_price) * quantity, 2)


    def compute_order_total_amount(self, cart_items: List[CartItem]) -> float:
        return round(
            sum(
                self.compute_item_total_price(item.product.price, item.quantity)
                for item in cart_items
            ),
            2,
        )


    def _build_order_items_from_cart(self, cart_items: List[CartItem]) -> List[OrderItem]:
        return [
            OrderItem(
                product_id=cart_item.product.id,
                store_id=cart_item.store.id,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price,
                total_price=self.compute_item_total_price(
                    cart_item.product.price,
                    cart_item.quantity,
                ),
            )
            for cart_item in cart_items
        ]


    def create_order(self, order: Order) -> Order:
        return self.order_repository.create_order(order)


    def create_order_items(self, cart_items: List[CartItem], order_id: int) -> List[OrderItem]:
        order_items = self._build_order_items_from_cart(cart_items)
        for order_item in order_items:
            order_item.order_id = order_id
        return self.order_repository.create_order_items(order_items)



    def complete_order(self, user_id: int, order_data: CreateOrderSchema) -> Order:
        cart = self.cart_service.get_cart_by_user_id(user_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        self.validate_cart(cart)

        total_amount = self.compute_order_total_amount(cart.items)
        order = Order(
            user_id=user_id,
            status=OrderStatus.PENDING,
            address_id=order_data.address_id,
            total_amount=total_amount,
        )
        order_items = self._build_order_items_from_cart(cart.items)

        try:
            new_order = self.order_repository.stage_order_with_items(order, order_items)
            self.cart_repository.clear_cart_without_commit(cart.id)
            self.db.commit()
            self.db.refresh(new_order)
            for order_item in order_items:
                self.db.refresh(order_item)
        except Exception:
            self.db.rollback()
            raise

        return new_order

    def get_orders_by_user_id(self, user_id: int) -> List[Order]:
        return self.order_repository.get_orders_by_user_id(user_id)


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(
        db=db,
        order_repository=get_order_repository(db),
        cart_repository=get_cart_repository(db),
        cart_service=get_cart_service(db),
        product_service=get_product_service(db),
        stock_service=get_stock_service(db),
    )
