from sqlalchemy import Column, Integer, String, DateTime, Enum as SQlEnum, Boolean, ForeignKey
from Core.Database.AsyncDatabase import Base
from datetime import datetime, timedelta
from enum import Enum
from sqlalchemy.orm import validates
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import relationship

class Role(Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(SQlEnum(Role), nullable=False, default=Role.USER)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        CheckConstraint(
            "phone ~ '^[0-9]{10}$'",
            name='check_phone_valid'
        ),
    )

    addresses = relationship("Address", back_populates="user")
    orders = relationship("Order", back_populates="user")
    cart = relationship("Cart", back_populates="user")
    activation_tokens = relationship("ActivationToken", back_populates="user")



class ActivationToken(Base):
    __tablename__ = "activation_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, unique=True)
    token = Column(String, nullable=False, index=True, unique=True)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, default=datetime.now() + timedelta(minutes=15))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="activation_tokens")

    __table_args__ = (
        CheckConstraint(
            "expires_at > created_at",
            name='check_expires_at_greater_than_created_at'
        ),
    )