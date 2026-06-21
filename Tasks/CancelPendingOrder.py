import logging

import Core.CeleryBootstrap  # noqa: F401 — ensure mappers before task runs

from Core.CeleryApp import celery_app
from Core.SyncDatabase import get_sync_session
from Modules.Order.Services.OrderCancellationServiceSync import OrderCancellationServiceSync

logger = logging.getLogger(__name__)


@celery_app.task
def cancel_pending_order(expiration_minutes: int = 10) -> int:
    with get_sync_session() as session:
        cancellation_service = OrderCancellationServiceSync(session)
        cancelled_count = cancellation_service.cancel_expired_pending_payment_orders(
            expiration_minutes
        )
        logger.info("Cancelled %s expired pending-payment orders", cancelled_count)
        return cancelled_count
