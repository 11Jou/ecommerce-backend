from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from Core.Database import get_db
from Modules.Order.Models import Order, OrderItem, OrderStatus

class IOrderRepository(ABC):
    @abstractmethod
    async def create_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def get_orders_by_user_id(self, user_id: int) -> List[Order]:
        pass

    @abstractmethod
    async def get_order_by_id(self, order_id: int, user_id: int) -> Order:
        pass

    @abstractmethod
    async def check_order_by_address_id(self, address_id: int) -> Order | None:
        pass

    @abstractmethod
    async def get_all_orders(self) -> List[Order]:
        pass

    @abstractmethod
    async def update_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def delete_order(self, order: Order) -> None:
        pass

    @abstractmethod
    async def add_order_items(self, order_items: List[OrderItem]) -> List[OrderItem]:
        pass

    @abstractmethod
    async def get_order_item_by_id(self, order_item_id: int) -> OrderItem:
        pass

    @abstractmethod
    async def get_expired_pending_payment_orders(self, expiration_minutes: int = 10) -> List[Order]:
        pass


class OrderRepository(IOrderRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order: Order) -> Order:
        self.db.add(order)
        await self.db.flush()
        return order

    async def get_orders_by_user_id(self, user_id: int) -> List[Order]:
        items_loader = joinedload(Order.items)
        product_loader = items_loader.joinedload(OrderItem.product)
        store_loader = items_loader.joinedload(OrderItem.store)
        address_loader = joinedload(Order.address)
        user_loader = joinedload(Order.user)

        result = await self.db.execute(
            select(Order)
            .options(
                items_loader,
                product_loader,
                store_loader,
                address_loader,
                user_loader,
            )
            .where(Order.user_id == user_id)
        )
        return list(result.unique().scalars().all())

    async def get_order_by_id(self, order_id: int, user_id: int) -> Order | None:
        items_loader = joinedload(Order.items)
        product_loader = items_loader.joinedload(OrderItem.product)
        store_loader = items_loader.joinedload(OrderItem.store)
        address_loader = joinedload(Order.address)
        user_loader = joinedload(Order.user)
        result = await self.db.execute(
            select(Order)
            .options(items_loader, product_loader, store_loader, address_loader, user_loader)
            .where(Order.id == order_id, Order.user_id == user_id)
        )
        return result.unique().scalars().first()

    async def check_order_by_address_id(self, address_id: int) -> Order | None:
        result = await self.db.execute(select(Order).where(Order.address_id == address_id))
        return result.scalars().first()

    async def get_all_orders(self) -> List[Order]:
        result = await self.db.execute(select(Order))
        return list(result.scalars().all())

    async def update_order(self, order: Order) -> Order:
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def delete_order(self, order: Order) -> None:
        await self.db.delete(order)
        await self.db.commit()

    async def add_order_items(self, order_items: List[OrderItem]) -> List[OrderItem]:
        self.db.add_all(order_items)
        return order_items

    async def get_order_item_by_id(self, order_item_id: int) -> OrderItem:
        result = await self.db.execute(select(OrderItem).where(OrderItem.id == order_item_id))
        return result.scalars().first()

    async def get_expired_pending_payment_orders(self, expiration_minutes: int = 10) -> List[Order]:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=expiration_minutes)
        items_loader = joinedload(Order.items)
        result = await self.db.execute(
            select(Order)
            .options(items_loader)
            .where(
                Order.status == OrderStatus.PENDING_PAYMENT,
                Order.created_at < cutoff,
            )
        )
        return list(result.unique().scalars().all())

def get_order_repository(db: AsyncSession = Depends(get_db)) -> IOrderRepository:
    return OrderRepository(db)
