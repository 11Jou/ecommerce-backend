import asyncio
import logging

from Core.CeleryApp import celery_app
from Core.Database import AsyncSessionLocal
from Modules.Order.Repository.OrderRepository import OrderRepository
from Modules.Order.Services.OrderCancellationService import OrderCancellationService
from Modules.Payment.Repository import PaymentRepository
from Modules.Stock.Repository.StockRepository import StockRepository
from Modules.Stock.Services.StockService import StockService

logger = logging.getLogger(__name__)


async def cancel_pending_order_task(expiration_minutes: int = 10) -> int:
    async with AsyncSessionLocal() as session:
        order_repository = OrderRepository(session)
        stock_service = StockService(StockRepository(session))
        payment_repository = PaymentRepository(session)
        cancellation_service = OrderCancellationService(
            db=session,
            order_repository=order_repository,
            stock_service=stock_service,
            payment_repository=payment_repository,
        )
        cancelled_count = await cancellation_service.cancel_expired_pending_payment_orders(
            expiration_minutes
        )
        logger.info("Cancelled %s expired pending-payment orders", cancelled_count)
        return cancelled_count


@celery_app.task
def cancel_pending_order(expiration_minutes: int = 10) -> int:
    return asyncio.run(cancel_pending_order_task(expiration_minutes))
