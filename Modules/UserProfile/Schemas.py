from pydantic import BaseModel
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