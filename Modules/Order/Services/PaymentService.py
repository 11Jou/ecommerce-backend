class IPaymentService(ABC):
    @abstractmethod
    def pay_order(self, order: Order) -> Payment:
        pass




class StripePaymentService(IPaymentService):

    
    def __init__(self, stripe_secret_key: str):
        self.stripe_secret_key = stripe_secret_key

    def pay_order(self, order: Order) -> Payment:
        pass


class CashPaymentService(IPaymentService):
    def pay_order(self, order: Order) -> Payment:
        pass