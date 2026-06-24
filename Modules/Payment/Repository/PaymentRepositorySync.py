from sqlalchemy import select
from sqlalchemy.orm import Session

from Modules.Payment.Models import Payment


class PaymentRepositorySync:
    def __init__(self, db: Session):
        self.db = db

    def get_payment_by_order_id(self, order_id: int) -> Payment | None:
        result = self.db.execute(select(Payment).where(Payment.order_id == order_id))
        return result.scalars().first()
