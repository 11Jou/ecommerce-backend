from fastapi import HTTPException

from Modules.Order.Services.PaymentMethods.Base import IPaymentMethodHandler
from Modules.Order.Services.PaymentMethods.CashOnDeliveryHandler import CashOnDeliveryHandler
from Modules.Order.Services.PaymentMethods.OnlinePaymentHandler import OnlinePaymentHandler
from Modules.Payment.Models import PaymentMethod


class PaymentMethodHandlerFactory:
    _registry = {
        PaymentMethod.CASH_ON_DELIVERY: CashOnDeliveryHandler,
        PaymentMethod.ONLINE_PAYMENT: OnlinePaymentHandler,
    }

    @classmethod
    def create(cls, method: PaymentMethod) -> IPaymentMethodHandler:
        handler_cls = cls._registry.get(method)
        if handler_cls is None:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported payment method: {method}",
            )
        return handler_cls()
