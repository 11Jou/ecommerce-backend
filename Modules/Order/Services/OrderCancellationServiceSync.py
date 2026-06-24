from sqlalchemy.orm import Session

from Modules.Order.Models import Order, OrderStatus
from Modules.Order.Repository.OrderRepositorySync import OrderRepositorySync
from Modules.Payment.Models import PaymentStatus
from Modules.Payment.Repository.PaymentRepositorySync import PaymentRepositorySync
from Modules.Stock.Repository.StockRepositorySync import StockRepositorySync


class OrderCancellationServiceSync:
    def __init__(self, db: Session):
        self.db = db
        self.order_repository = OrderRepositorySync(db)
        self.stock_repository = StockRepositorySync(db)
        self.payment_repository = PaymentRepositorySync(db)

    def _claim_order_for_cancellation(self, order: Order) -> bool:
        self.db.refresh(order)
        if order.status != OrderStatus.PENDING_PAYMENT:
            return False
        order.status = OrderStatus.CANCELING
        self.db.commit()
        return True

    def _finalize_cancellation(self, order: Order) -> None:
        payment = self.payment_repository.get_payment_by_order_id(order.id)
        if payment and payment.status == PaymentStatus.PENDING:
            payment.status = PaymentStatus.CANCELLED

        order.status = OrderStatus.CANCELLED
        self.db.commit()

    def cancel_expired_pending_payment_orders(self, expiration_minutes: int = 10) -> int:
        orders = self.order_repository.get_expired_pending_payment_orders(expiration_minutes)
        if not orders:
            return 0

        cancelled_count = 0
        for order in orders:
            try:
                if not self._claim_order_for_cancellation(order):
                    continue

                for item in order.items:
                    self.stock_repository.release_stock(
                        item.product_id, item.store_id, item.quantity
                    )

                self._finalize_cancellation(order)
                cancelled_count += 1
            except Exception:
                self.db.rollback()
                order.status = OrderStatus.PENDING_PAYMENT
                self.db.commit()
                raise

        return cancelled_count
