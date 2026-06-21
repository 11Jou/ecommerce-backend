from datetime import datetime, timedelta, timezone
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from Modules.Order.Models import Order, OrderItem, OrderStatus


class OrderRepositorySync:
    def __init__(self, db: Session):
        self.db = db

    def get_expired_pending_payment_orders(self, expiration_minutes: int = 10) -> List[Order]:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=expiration_minutes)
        items_loader = joinedload(Order.items)
        result = self.db.execute(
            select(Order)
            .options(items_loader)
            .where(
                Order.status == OrderStatus.PENDING_PAYMENT,
                Order.created_at < cutoff,
            )
        )
        return list(result.unique().scalars().all())
