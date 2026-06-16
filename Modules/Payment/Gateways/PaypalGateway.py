from Modules.Payment.Schemas import CardDetailsSchema
from Modules.Payment.Gateways.Base import IOnlinePaymentGateway, PaymentResult


class PaypalGateway(IOnlinePaymentGateway):
    def charge(self, amount: float, card: CardDetailsSchema) -> PaymentResult:
        last4 = card.card_number[-4:] if card.card_number else "****"
        return PaymentResult(
            success=True,
            reference=f"sim_paypal_{last4}",
            message="PayPal payment simulated successfully",
        )
