from sqlalchemy.sql import func
from sqlalchemy.schema import CheckConstraint
from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime, Enum as SQlEnum
from sqlalchemy.orm import relationship
from Core.Database.AsyncDatabase import Base
from enum import Enum

class PaymentMethod(Enum):
    CASH_ON_DELIVERY = "cash_on_delivery"
    ONLINE_PAYMENT = "online_payment"


class OnlineProvider(Enum):
    STRIPE = "stripe"
    PAYPAL = "paypal"


class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"
    REFUND_FAILED = "refund_failed"
    REFUND_PENDING = "refund_pending"



class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    payment_method = Column(SQlEnum(PaymentMethod), nullable=False)
    provider = Column(SQlEnum(OnlineProvider), nullable=True)
    status = Column(SQlEnum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    order = relationship("Order", back_populates="payments")