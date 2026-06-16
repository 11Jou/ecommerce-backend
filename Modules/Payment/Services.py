from fastapi import Depends
from sqlalchemy.orm import Session

from Core.Database import get_db
from Modules.Payment.Models import Payment
from Modules.Payment.Repository import IPaymentRepository, get_payment_repository


class PaymentService:

    def __init__(self, payment_repository: IPaymentRepository):
        self.payment_repository = payment_repository

    def create_payment(self, payment: Payment) -> Payment:
        return self.payment_repository.create_payment(payment)

    def add_payment(self, payment: Payment) -> Payment:
        return self.payment_repository.add_payment(payment)

    def get_payment_by_id(self, payment_id: int) -> Payment:
        return self.payment_repository.get_payment_by_id(payment_id)

    def update_payment(self, payment: Payment) -> Payment:
        return self.payment_repository.update_payment(payment)

    def delete_payment(self, payment_id: int) -> None:
        return self.payment_repository.delete_payment(payment_id)


def get_payment_service(db: Session = Depends(get_db)) -> PaymentService:
    return PaymentService(get_payment_repository(db))
