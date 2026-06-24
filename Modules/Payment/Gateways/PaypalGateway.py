from Modules.Payment.Schemas import CardDetailsSchema
from Modules.Payment.Gateways.Base import IOnlinePaymentGateway, PaymentIntentResult
from Modules.Order.Models import Order
from Modules.Payment.Models import Payment


class PaypalGateway(IOnlinePaymentGateway):


    def pay(self, amount: float) -> PaymentIntentResult:
        pass
