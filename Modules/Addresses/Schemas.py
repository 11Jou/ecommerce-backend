from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CreateAddressSchema(BaseModel):
    city: str
    street: str
    building: str
    additional_info: Optional[str] = None


class UpdateAddressSchema(BaseModel):
    city: Optional[str] = None
    street: Optional[str] = None
    building: Optional[str] = None
    additional_info: Optional[str] = None

class AddressSchema(BaseModel):
    id: int
    city: str
    street: str
    building: str
    additional_info: Optional[str] = None
    created_at: datetime
    updated_at: datetime