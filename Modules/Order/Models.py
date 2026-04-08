from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey , Boolean, Enum as SQlEnum
from Core.Database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import CheckConstraint
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"



class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    building = Column(String, nullable=False)
    additional_info = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="address")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False, index=True)
    status = Column(SQlEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="orders")
    address = relationship("Address", back_populates="orders")



class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)


    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    __table_args__ = (
        CheckConstraint("quantity > 0"),
        CheckConstraint("unit_price > 0"),
    )


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_items"

    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")