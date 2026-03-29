from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class UserProfileResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    created_at: datetime
    updated_at: datetime


class UpdateUserProfile(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None


    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.isdigit() or len(v) != 10:
            raise ValueError("Phone number must be 10 digits")
        return v

