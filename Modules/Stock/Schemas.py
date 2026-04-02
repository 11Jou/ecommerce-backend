from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional

class CategorySchema(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CreateCategorySchema(BaseModel):
    name: str
    description: str
    is_active: bool = True


class UpdateCategorySchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if self.name is None and self.description is None and self.is_active is None:
            raise ValueError("At least one field must be provided for update")
        return self


class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ProductStoreAvailabilitySchema(BaseModel):
    store_id: int
    store_name: str
    quantity: int


class ProductWithAvailabilitySchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    availability: list[ProductStoreAvailabilitySchema]


class CreateProductSchema(BaseModel):
    name: str
    description: str
    price: float
    category_id: int
    is_active: bool = True


class UpdateProductSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if self.name is None and self.description is None and self.price is None and self.category_id is None and self.is_active is None:
            raise ValueError("At least one field must be provided for update")
        return self

class StoreSchema(BaseModel):
    id: int
    name: str
    address: str
    created_at: datetime
    updated_at: datetime

class CreateStoreSchema(BaseModel):
    name: str
    address: str

class UpdateStoreSchema(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if self.name is None and self.address is None:
            raise ValueError("At least one field must be provided for update")
        return self


class StockSchema(BaseModel):
    store_id: int
    product_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime

class CreateStockSchema(BaseModel):
    store_id: int
    product_id: int
    quantity: int


class UpdateStockSchema(BaseModel):
    quantity: int
