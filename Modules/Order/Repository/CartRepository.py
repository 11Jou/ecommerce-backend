from abc import ABC, abstractmethod

from sqlalchemy.orm import Session, joinedload
from Modules.Order.Models import Cart, CartItem
from fastapi import Depends, HTTPException
from Core.Database import get_db
from typing import List
from sqlalchemy.exc import IntegrityError

class ICartRepository(ABC):
    @abstractmethod
    def create_cart(self, cart: Cart) -> Cart:
        pass

    @abstractmethod
    def get_cart_by_id(self, cart_id: int) -> Cart:
        pass

    @abstractmethod
    def get_cart_or_create(self, user_id: int) -> Cart:
        pass

    @abstractmethod
    def get_cart_by_user_id(self, user_id: int) -> Cart:
        pass

    @abstractmethod
    def get_cart_item_by_id(self, cart_item_id: int) -> CartItem:
        pass

    @abstractmethod
    def get_cart_item_by_product_id_and_cart_id(self, product_id: int, store_id: int, cart_id: int) -> CartItem:
        pass

    @abstractmethod
    def delete_cart(self, cart: Cart) -> None:
        pass

    @abstractmethod
    def create_cart_item(self, cart_item: CartItem) -> CartItem:
        pass

    @abstractmethod
    def remove_item_from_cart(self, cart_item_id: int) -> None:
        pass

    @abstractmethod
    def update_item_quantity(self, cart_item_id: int, quantity: int) -> CartItem:
        pass

    @abstractmethod
    def clear_cart(self, cart_id: int) -> None:
        pass

    @abstractmethod
    def clear_cart_without_commit(self, cart_id: int) -> None:
        pass

    @abstractmethod
    def get_all_items_in_cart(self, cart_id: int) -> List[CartItem]:
        pass


class CartRepository(ICartRepository):

    def __init__(self, db: Session):
        self.db = db

    def create_cart(self, cart: Cart) -> Cart:
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    def get_cart_item_by_id(self, cart_item_id: int) -> CartItem:
        return self.db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    def get_cart_or_create(self, user_id: int) -> Cart:
        cart = self.get_cart_by_user_id(user_id)

        if cart:
            return cart
        cart = Cart(user_id=user_id)
        self.db.add(cart)

        try:
            self.db.commit()
            self.db.refresh(cart)
        except IntegrityError as e:
            self.db.rollback()
            cart = self.get_cart_by_user_id(user_id)
        return cart




    def get_cart_by_id(self, cart_id: int) -> Cart:
        return (
            self.db.query(Cart)
            .options(
                joinedload(Cart.items)
                .joinedload(CartItem.product)
                .joinedload(CartItem.store)
            )
            .filter(Cart.id == cart_id)
            .first()
        )

    def get_cart_by_user_id(self, user_id: int) -> Cart:
        return (
            self.db.query(Cart)
            .options(
                joinedload(Cart.items)
                .joinedload(CartItem.product)
                .joinedload(CartItem.store)
            )
            .filter(Cart.user_id == user_id)
            .first()
        )

    def get_cart_item_by_product_id_and_cart_id(self, product_id: int, store_id: int, cart_id: int) -> CartItem:
        return self.db.query(CartItem).filter(CartItem.product_id == product_id, CartItem.store_id == store_id, CartItem.cart_id == cart_id).first()

    def update_cart_item(self, cart_item: CartItem) -> CartItem:
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def delete_cart(self, cart: Cart) -> None:
        self.db.delete(cart)
        self.db.commit()

    def create_cart_item(self, cart_item: CartItem) -> CartItem:
        self.db.add(cart_item)
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def remove_item_from_cart(self, cart_item_id: int) -> None:
        cart_item = self.db.query(CartItem).filter(CartItem.id == cart_item_id).first()
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        self.db.delete(cart_item)
        self.db.commit()

    def update_item_quantity(self, cart_item_id: int, quantity: int) -> CartItem:
        cart_item = self.db.query(CartItem).filter(CartItem.id == cart_item_id).first()
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")

        cart_item.quantity = quantity
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def clear_cart_without_commit(self, cart_id: int) -> None:
        cart_items = self.db.query(CartItem).filter(CartItem.cart_id == cart_id).all()
        for cart_item in cart_items:
            self.db.delete(cart_item)

    def clear_cart(self, cart_id: int) -> None:
        self.clear_cart_without_commit(cart_id)
        self.db.commit()



def get_cart_repository(db: Session = Depends(get_db)) -> CartRepository:
    return CartRepository(db)