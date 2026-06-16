from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from Core.Database import get_db
from Modules.Payment.Models import Payment


class IPaymentRepository(ABC):

    @abstractmethod
    def create_payment(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def add_payment(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def get_payment_by_id(self, payment_id: int) -> Payment:
        pass

    @abstractmethod
    def update_payment(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def delete_payment(self, payment_id: int) -> None:
        pass

    @abstractmethod
    def get_all_payments(self) -> List[Payment]:
        pass


class PaymentRepository(IPaymentRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_payment(self, payment: Payment) -> Payment:
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def add_payment(self, payment: Payment) -> Payment:
        self.db.add(payment)
        self.db.flush()
        return payment

    def get_payment_by_id(self, payment_id: int) -> Payment:
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def update_payment(self, payment: Payment) -> Payment:
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def delete_payment(self, payment_id: int) -> None:
        self.db.query(Payment).filter(Payment.id == payment_id).delete()
        self.db.commit()

    def get_all_payments(self) -> List[Payment]:
        return self.db.query(Payment).all()


def get_payment_repository(db: Session = Depends(get_db)) -> IPaymentRepository:
    return PaymentRepository(db)