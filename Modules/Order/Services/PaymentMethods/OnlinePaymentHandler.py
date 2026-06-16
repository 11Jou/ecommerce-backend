from fastapi import HTTPException

from Modules.Order.Models import Order, OrderStatus
from Modules.Order.Schemas import CreateOrderSchema
from Modules.Order.Services.PaymentMethods.Base import IPaymentMethodHandler
from Modules.Payment.Gateways.Factory import OnlinePaymentGatewayFactory
from Modules.Payment.Models import Payment, PaymentMethod, PaymentStatus


class OnlinePaymentHandler(IPaymentMethodHandler):
    def process(self, order: Order, order_data: CreateOrderSchema) -> Payment:
        gateway = OnlinePaymentGatewayFactory.create(order_data.online_provider)
        result = gateway.charge(float(order.total_amount), order_data.card_details)

        if not result.success:
            raise HTTPException(status_code=400, detail="Online payment failed")

        order.status = OrderStatus.PENDING_PAYMENT
        return Payment(
            order_id=order.id,
            payment_method=PaymentMethod.ONLINE_PAYMENT,
            provider=order_data.online_provider,
            status=PaymentStatus.PENDING,
        )
