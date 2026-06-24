from Modules.Payment.Gateways.Base import IOnlinePaymentGateway, PaymentIntentResult
from Core.settings import get_stripe_secret_key
from Modules.Order.Models import Order
from Modules.Payment.Models import Payment
import stripe

class StripeGateway(IOnlinePaymentGateway):

    def __init__(self):
        self.client = stripe
        self.client.api_key = get_stripe_secret_key()


    def pay(self, amount: float) -> PaymentIntentResult:
        intent = self.client.PaymentIntent.create(
            amount=int(amount * 100),
            currency="usd",
        )        
        return PaymentIntentResult(
            payment_intent_id=intent.id,
            client_secret=intent.client_secret,
        )