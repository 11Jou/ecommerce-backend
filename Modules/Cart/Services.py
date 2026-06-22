from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Database.AsyncDatabase import get_db
from Modules.Cart.Models import Cart, CartItem
from Modules.Cart.Repository import ICartRepository, get_cart_repository
from Modules.Cart.Schemas import CreateCartItemSchema
from Modules.Stock.Services.ProductService import ProductService, get_product_service
from Modules.Stock.Services.StockService import StockService, get_stock_service


class CartService:
    def __init__(
        self,
        cart_repository: ICartRepository,
        product_service: ProductService,
        stock_service: StockService,
    ):
        self.cart_repository = cart_repository
        self.product_service = product_service
        self.stock_service = stock_service

    async def get_cart_by_user_id(self, user_id: int) -> Cart:
        return await self.cart_repository.get_cart_by_user_id(user_id)

    async def get_cart_by_id(self, cart_id: int) -> Cart:
        cart = await self.cart_repository.get_cart_by_id(cart_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        return cart

    async def get_cart_or_create(self, user_id: int) -> Cart:
        return await self.cart_repository.get_cart_or_create(user_id)

    async def create_cart(self, user_id: int) -> Cart:
        new_cart = Cart(user_id=user_id)
        return await self.cart_repository.create_cart(new_cart)

    async def create_cart_item(self, cart_item: CreateCartItemSchema, cart_id: int) -> CartItem:
        product = await self.product_service.get_product_by_id(cart_item.product_id)

        if not product.is_active:
            raise HTTPException(status_code=400, detail="Product is not active")

        existing_item = await self.cart_repository.get_cart_item_by_product_id_and_cart_id(
            cart_item.product_id,
            cart_item.store_id,
            cart_id,
        )
        if existing_item:
            total_quantity = existing_item.quantity + cart_item.quantity

            await self.stock_service.check_stock_availability(
                cart_item.product_id, cart_item.store_id, total_quantity
            )

            return await self.cart_repository.update_item_quantity(
                existing_item.id,
                total_quantity,
            )
        await self.stock_service.check_stock_availability(
            cart_item.product_id, cart_item.store_id, cart_item.quantity
        )

        new_item = CartItem(
            cart_id=cart_id,
            product_id=cart_item.product_id,
            store_id=cart_item.store_id,
            quantity=cart_item.quantity,
        )

        return await self.cart_repository.create_cart_item(new_item)

    async def remove_item_from_cart(self, cart_item_id: int) -> None:
        return await self.cart_repository.remove_item_from_cart(cart_item_id)

    async def update_item_quantity(self, cart_item_id: int, quantity: int) -> CartItem:
        cart_item = await self.cart_repository.get_cart_item_by_id(cart_item_id)
        await self.stock_service.check_stock_availability(
            cart_item.product_id, cart_item.store_id, quantity
        )
        return await self.cart_repository.update_item_quantity(cart_item_id, quantity)

    async def clear_cart_without_commit(self, cart_id: int) -> None:
        return await self.cart_repository.clear(cart_id)

    async def clear_cart(self, cart_id: int) -> None:
        return await self.cart_repository.clear_cart(cart_id)

    def validate_cart(self, cart: Cart) -> None:
        if not cart or not cart.items:
            raise HTTPException(status_code=400, detail="Cart is empty")
        for item in cart.items:
            if item.quantity <= 0:
                raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
            if not item.product.is_active:
                raise HTTPException(status_code=400, detail="Product is not active")


def get_cart_service(db: AsyncSession = Depends(get_db)) -> CartService:
    return CartService(get_cart_repository(db), get_product_service(db), get_stock_service(db))
