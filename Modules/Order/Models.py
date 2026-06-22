from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey , Boolean, Enum as SQlEnum
from Core.Database.AsyncDatabase import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import CheckConstraint, UniqueConstraint
from enum import Enum

class OrderStatus(Enum):
    PENDING_PAYMENT = "pending_payment"
    PAYMENT_PROCESSING = "payment_processing"
    PENDING_SHIPMENT = "pending_shipment"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"
    COMPLETED = "completed"
    CANCELING = "canceling"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False, index=True)
    status = Column(SQlEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING_PAYMENT)
    total_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="orders")
    address = relationship("Address", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")



class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    store = relationship("Store", back_populates="order_items")

    __table_args__ = (
        UniqueConstraint("order_id", "product_id", "store_id", name="uix_order_product_store"),
        CheckConstraint('quantity > 0', name='quantity_check'),
        CheckConstraint('unit_price > 0', name='unit_price_check'),
        CheckConstraint('total_price > 0', name='total_price_check'),
    )