from Modules.Order.Models import Order, OrderStatus
from Modules.Order.Schemas import CreateOrderSchema
from Modules.Order.Services.PaymentMethods.Base import IPaymentMethodHandler
from Modules.Payment.Models import Payment, PaymentMethod, PaymentStatus


class CashOnDeliveryHandler(IPaymentMethodHandler):
    def process(self, order: Order, order_data: CreateOrderSchema) -> Payment:
        order.status = OrderStatus.PENDING_SHIPMENT
        return Payment(
            order_id=order.id,
            payment_method=PaymentMethod.CASH_ON_DELIVERY,
            status=PaymentStatus.PENDING,
        )
