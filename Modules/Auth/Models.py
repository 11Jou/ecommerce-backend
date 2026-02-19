from sqlalchemy import Column, Integer, String, DateTime, Enum as SQlEnum
from Core.Database import Base
from datetime import datetime
from enum import Enum


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