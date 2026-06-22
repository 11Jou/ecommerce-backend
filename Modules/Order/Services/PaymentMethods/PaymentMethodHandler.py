from abc import ABC, abstractmethod
from Modules.Order.Models import Order, OrderStatus
from Modules.Payment.Models import Payment, PaymentMethod, PaymentStatus

class IPaymentMethodHandler(ABC):
    @abstractmethod
    def process(self, order: Order) -> Payment:
        pass


class CashOnDeliveryHandler(IPaymentMethodHandler):
    def process(self, order: Order) -> Payment:
        order.status = OrderStatus.PENDING_SHIPMENT
        return Payment(
            order_id=order.id,
            payment_method=PaymentMethod.CASH_ON_DELIVERY,
            status=PaymentStatus.PENDING,
        )


class OnlinePaymentHandler(IPaymentMethodHandler):
    def process(self, order: Order) -> Payment:
        order.status = OrderStatus.PENDING_PAYMENT
        return Payment(
            order_id=order.id,
            payment_method=PaymentMethod.ONLINE_PAYMENT,
            status=PaymentStatus.PENDING,
        )
