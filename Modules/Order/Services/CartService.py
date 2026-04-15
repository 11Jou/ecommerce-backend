from Modules.Order.Repository.CartRepository import ICartRepository, get_cart_repository
from Modules.Order.Models import Cart, CartItem
from fastapi import Depends
from Core.Database import get_db
from sqlalchemy.orm import Session
from typing import List

class CartService:

    def __init__(self, cart_repository: ICartRepository):
        self.cart_repository = cart_repository

    def get_cart_by_user_id(self, user_id: int) -> Cart:
        return self.cart_repository.get_cart_by_user_id(user_id)

    def create_cart(self, user_id: int) -> Cart:
        new_cart = Cart(user_id=user_id)
        return self.cart_repository.create_cart(new_cart)

    def create_cart_item(self, cart_item: CartItem) -> CartItem:
        new_cart_item = CartItem(cart_id=cart_item.cart_id, 
        product_id=cart_item.product_id, 
        quantity=cart_item.quantity)
        return self.cart_repository.create_cart_item(new_cart_item)

    def remove_item_from_cart(self, cart_item_id: int) -> None:
        return self.cart_repository.remove_item_from_cart(cart_item_id)

    def update_item_quantity(self, cart_item_id: int, quantity: int) -> CartItem:
        return self.cart_repository.update_item_quantity(cart_item_id, quantity)

    def clear_cart(self, cart_id: int) -> None:
        return self.cart_repository.clear_cart(cart_id)

    def get_all_items_in_cart(self, cart_id: int) -> List[CartItem]:
        return self.cart_repository.get_all_items_in_cart(cart_id)


def get_cart_service(db: Session = Depends(get_db)) -> CartService:
    return CartService(get_cart_repository(db))