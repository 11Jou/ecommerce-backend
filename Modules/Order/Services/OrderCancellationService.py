from datetime import datetime, timedelta, timezone
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from Modules.Order.Models import Order, OrderItem, OrderStatus
from Modules.Order.Repository.OrderRepository import IOrderRepository
from Modules.Payment.Models import PaymentStatus
from Modules.Payment.Repository import IPaymentRepository
from Modules.Stock.Services.StockService import StockService


class OrderCancellationService:
    def __init__(
        self,
        db: AsyncSession,
        order_repository: IOrderRepository,
        stock_service: StockService,
        payment_repository: IPaymentRepository,
    ):
        self.db = db
        self.order_repository = order_repository
        self.stock_service = stock_service
        self.payment_repository = payment_repository

    async def cancel_expired_pending_payment_orders(self, expiration_minutes: int = 10) -> int:
        orders = await self.order_repository.get_expired_pending_payment_orders(expiration_minutes)
        if not orders:
            return 0

        try:
            for order in orders:
                for item in order.items:
                    await self.stock_service.release_stock(
                        item.product_id, item.store_id, item.quantity
                    )

                payment = await self.payment_repository.get_payment_by_order_id(order.id)
                if payment and payment.status == PaymentStatus.PENDING:
                    payment.status = PaymentStatus.CANCELLED

                order.status = OrderStatus.CANCELLED

            await self.db.commit()
            return len(orders)
        except Exception:
            await self.db.rollback()
            raise
