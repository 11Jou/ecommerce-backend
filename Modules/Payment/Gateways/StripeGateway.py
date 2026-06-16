from Modules.Payment.Schemas import CardDetailsSchema
from Modules.Payment.Gateways.Base import IOnlinePaymentGateway, PaymentResult


class StripeGateway(IOnlinePaymentGateway):
    def charge(self, amount: float, card: CardDetailsSchema) -> PaymentResult:
        last4 = card.card_number[-4:] if card.card_number else "****"
        return PaymentResult(
            success=True,
            reference=f"sim_stripe_{last4}",
            message="Stripe payment simulated successfully",
        )
