from abc import ABC, abstractmethod

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from Core.Database.AsyncDatabase import get_db
from Modules.Cart.Models import Cart, CartItem
from Modules.Stock.Models import Product


class ICartRepository(ABC):
    @abstractmethod
    async def create_cart(self, cart: Cart) -> Cart:
        pass

    @abstractmethod
    async def get_cart_by_id(self, cart_id: int) -> Cart:
        pass

    @abstractmethod
    async def get_cart_or_create(self, user_id: int) -> Cart:
        pass

    @abstractmethod
    async def get_cart_by_user_id(self, user_id: int) -> Cart:
        pass

    @abstractmethod
    async def get_cart_item_by_id(self, cart_item_id: int) -> CartItem:
        pass

    @abstractmethod
    async def get_cart_item_by_product_id_and_cart_id(
        self, product_id: int, store_id: int, cart_id: int
    ) -> CartItem:
        pass

    @abstractmethod
    async def delete_cart(self, cart: Cart) -> None:
        pass

    @abstractmethod
    async def create_cart_item(self, cart_item: CartItem) -> CartItem:
        pass

    @abstractmethod
    async def remove_item_from_cart(self, cart_item_id: int) -> None:
        pass

    @abstractmethod
    async def update_item_quantity(self, cart_item_id: int, quantity: int) -> CartItem:
        pass

    @abstractmethod
    async def clear(self, cart_id: int) -> None:
        pass

    @abstractmethod
    async def clear_cart(self, cart_id: int) -> None:
        pass


class CartRepository(ICartRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_cart(self, cart: Cart) -> Cart:
        self.db.add(cart)
        await self.db.commit()
        await self.db.refresh(cart)
        return cart

    async def get_cart_item_by_id(self, cart_item_id: int) -> CartItem:
        result = await self.db.execute(select(CartItem).where(CartItem.id == cart_item_id))
        return result.scalars().first()

    async def get_cart_or_create(self, user_id: int) -> Cart:
        cart = await self.get_cart_by_user_id(user_id)

        if cart:
            return cart
        cart = Cart(user_id=user_id)
        self.db.add(cart)

        try:
            await self.db.commit()
            await self.db.refresh(cart)
        except IntegrityError:
            await self.db.rollback()
            cart = await self.get_cart_by_user_id(user_id)
        return cart

    async def get_cart_by_id(self, cart_id: int) -> Cart:
        items_loader = joinedload(Cart.items)
        product_loader = items_loader.joinedload(CartItem.product)
        category_loader = product_loader.joinedload(Product.category)
        store_loader = items_loader.joinedload(CartItem.store)
        result = await self.db.execute(
            select(Cart)
            .options(items_loader, product_loader, category_loader, store_loader)
            .where(Cart.id == cart_id)
        )
        return result.unique().scalars().first()

    async def get_cart_by_user_id(self, user_id: int) -> Cart:
        items_loader = joinedload(Cart.items)
        product_loader = items_loader.joinedload(CartItem.product)
        category_loader = product_loader.joinedload(Product.category)
        store_loader = items_loader.joinedload(CartItem.store)
        result = await self.db.execute(
            select(Cart)
            .options(items_loader, product_loader, category_loader, store_loader)
            .where(Cart.user_id == user_id)
        )
        return result.unique().scalars().first()

    async def get_cart_item_by_product_id_and_cart_id(
        self, product_id: int, store_id: int, cart_id: int
    ) -> CartItem:
        result = await self.db.execute(
            select(CartItem).where(
                CartItem.product_id == product_id,
                CartItem.store_id == store_id,
                CartItem.cart_id == cart_id,
            )
        )
        return result.scalars().first()

    async def update_cart_item(self, cart_item: CartItem) -> CartItem:
        await self.db.commit()
        await self.db.refresh(cart_item)
        return cart_item

    async def delete_cart(self, cart: Cart) -> None:
        await self.db.delete(cart)
        await self.db.commit()

    async def create_cart_item(self, cart_item: CartItem) -> CartItem:
        self.db.add(cart_item)
        await self.db.commit()
        await self.db.refresh(cart_item)
        return cart_item

    async def remove_item_from_cart(self, cart_item_id: int) -> None:
        cart_item = await self.get_cart_item_by_id(cart_item_id)
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        await self.db.delete(cart_item)
        await self.db.commit()

    async def update_item_quantity(self, cart_item_id: int, quantity: int) -> CartItem:
        cart_item = await self.get_cart_item_by_id(cart_item_id)
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")

        cart_item.quantity = quantity
        await self.db.commit()
        await self.db.refresh(cart_item)
        return cart_item

    async def clear(self, cart_id: int) -> None:
        result = await self.db.execute(select(CartItem).where(CartItem.cart_id == cart_id))
        cart_items = result.scalars().all()
        for cart_item in cart_items:
            await self.db.delete(cart_item)

    async def clear_cart(self, cart_id: int) -> None:
        await self.clear(cart_id)
        await self.db.commit()


def get_cart_repository(db: AsyncSession = Depends(get_db)) -> CartRepository:
    return CartRepository(db)
