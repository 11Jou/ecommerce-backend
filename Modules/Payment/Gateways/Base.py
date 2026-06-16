from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from Modules.Order.Schemas import CardDetailsSchema


@dataclass
class PaymentResult:
    success: bool
    reference: Optional[str] = None
    message: str = ""


class IOnlinePaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float, card: CardDetailsSchema) -> PaymentResult:
        pass
