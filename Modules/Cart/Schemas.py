from pydantic import BaseModel, Field

from Modules.Stock.Schemas import ProductSchema
from Modules.Stock.Schemas import StoreSchema


class CreateCartItemSchema(BaseModel):
    product_id: int
    store_id: int
    quantity: int = Field(ge=1)


class CartItemSchema(BaseModel):
    id: int
    product: ProductSchema
    quantity: int
    store: StoreSchema


class UpdateCartItemSchema(BaseModel):
    quantity: int = Field(ge=1)


class CartSchema(BaseModel):
    id: int
    user_id: int
    items: list[CartItemSchema]
