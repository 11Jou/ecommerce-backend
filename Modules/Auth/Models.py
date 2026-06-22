from sqlalchemy import Column, Integer, String, DateTime, Enum as SQlEnum
from Core.Database.AsyncDatabase import Base
from datetime import datetime
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