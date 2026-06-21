from sqlalchemy.ext.asyncio import AsyncSession

from Modules.Order.Models import Order, OrderStatus
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

    async def _claim_order_for_cancellation(self, order: Order) -> bool:
        await self.db.refresh(order)
        if order.status != OrderStatus.PENDING_PAYMENT:
            return False
        order.status = OrderStatus.CANCELING
        await self.db.commit()
        return True

    async def _finalize_cancellation(self, order: Order) -> None:
        payment = await self.payment_repository.get_payment_by_order_id(order.id)
        if payment and payment.status == PaymentStatus.PENDING:
            payment.status = PaymentStatus.CANCELLED

        order.status = OrderStatus.CANCELLED
        await self.db.commit()

    async def cancel_expired_pending_payment_orders(self, expiration_minutes: int = 10) -> int:
        orders = await self.order_repository.get_expired_pending_payment_orders(expiration_minutes)
        if not orders:
            return 0

        cancelled_count = 0
        for order in orders:
            try:
                if not await self._claim_order_for_cancellation(order):
                    continue

                for item in order.items:
                    await self.stock_service.release_stock(
                        item.product_id, item.store_id, item.quantity
                    )

                await self._finalize_cancellation(order)
                cancelled_count += 1
            except Exception:
                await self.db.rollback()
                order.status = OrderStatus.PENDING_PAYMENT
                await self.db.commit()
                raise

        return cancelled_count
