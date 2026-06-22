from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from Core.Database.AsyncDatabase import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

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