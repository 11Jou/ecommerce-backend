from fastapi import HTTPException

from Modules.Payment.Models import OnlineProvider
from Modules.Payment.Gateways.Base import IOnlinePaymentGateway
from Modules.Payment.Gateways.StripeGateway import StripeGateway
from Modules.Payment.Gateways.PaypalGateway import PaypalGateway


class OnlinePaymentGatewayFactory:
    _registry = {
        OnlineProvider.STRIPE: StripeGateway,
        OnlineProvider.PAYPAL: PaypalGateway,
    }

    @classmethod
    def create(cls, provider: OnlineProvider) -> IOnlinePaymentGateway:
        gateway_cls = cls._registry.get(provider)
        if gateway_cls is None:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported online payment provider: {provider}",
            )
        return gateway_cls()
