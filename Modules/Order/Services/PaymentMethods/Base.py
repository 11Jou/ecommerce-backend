from abc import ABC, abstractmethod

from Modules.Order.Models import Order
from Modules.Payment.Models import Payment


class IPaymentMethodHandler(ABC):
    @abstractmethod
    def process(self, order: Order) -> Payment:
        pass
