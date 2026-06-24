from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from Modules.Order.Models import Order
from Modules.Payment.Models import Payment
from Modules.Payment.Schemas import CardDetailsSchema


@dataclass
class PaymentIntentResult:
    payment_intent_id: str
    client_secret: str

class IOnlinePaymentGateway(ABC):

    @abstractmethod
    def pay(self, order: Order, payment: Payment) -> PaymentIntentResult:
        pass
