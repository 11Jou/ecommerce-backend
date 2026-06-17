from abc import ABC, abstractmethod
from typing import List

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Database import get_db
from Modules.Payment.Models import Payment


class IPaymentRepository(ABC):
    @abstractmethod
    async def create_payment(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    async def add_payment(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    async def get_payment_by_id(self, payment_id: int) -> Payment:
        pass

    @abstractmethod
    async def get_payment_by_order_id(self, order_id: int) -> Payment:
        pass

    @abstractmethod
    async def update_payment(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    async def delete_payment(self, payment_id: int) -> None:
        pass

    @abstractmethod
    async def get_all_payments(self) -> List[Payment]:
        pass


class PaymentRepository(IPaymentRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(self, payment: Payment) -> Payment:
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def add_payment(self, payment: Payment) -> Payment:
        self.db.add(payment)
        await self.db.flush()
        return payment

    async def get_payment_by_id(self, payment_id: int) -> Payment:
        result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        return result.scalars().first()

    async def get_payment_by_order_id(self, order_id: int) -> Payment:
        result = await self.db.execute(select(Payment).where(Payment.order_id == order_id))
        return result.scalars().first()

    async def update_payment(self, payment: Payment) -> Payment:
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def delete_payment(self, payment_id: int) -> None:
        await self.db.execute(delete(Payment).where(Payment.id == payment_id))
        await self.db.commit()

    async def get_all_payments(self) -> List[Payment]:
        result = await self.db.execute(select(Payment))
        return list(result.scalars().all())


def get_payment_repository(db: AsyncSession = Depends(get_db)) -> IPaymentRepository:
    return PaymentRepository(db)
