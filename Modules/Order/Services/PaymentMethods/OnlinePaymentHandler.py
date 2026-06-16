from Modules.Order.Models import Order, OrderStatus
from Modules.Order.Services.PaymentMethods.Base import IPaymentMethodHandler
from Modules.Payment.Models import Payment, PaymentMethod, PaymentStatus


class OnlinePaymentHandler(IPaymentMethodHandler):
    def process(self, order: Order) -> Payment:
        order.status = OrderStatus.PENDING_PAYMENT
        return Payment(
            order_id=order.id,
            payment_method=PaymentMethod.ONLINE_PAYMENT,
            status=PaymentStatus.PENDING,
        )
