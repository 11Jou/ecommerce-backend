from pydantic import BaseModel
from datetime import datetime

class CategorySchema(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class CreateCategorySchema(BaseModel):
    name: str


class UpdateCategorySchema(BaseModel):
    name: str