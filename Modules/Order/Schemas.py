from datetime import datetime
from Modules.Order.Models import OrderStatus
from pydantic import BaseModel, conint, Field
from Modules.Stock.Schemas import ProductSchema


class CreateCartItemSchema(BaseModel):
    product_id: int
    store_id: int
    quantity: int = Field(ge=1)

class CartItemSchema(BaseModel):
    id: int
    product: ProductSchema
    quantity: int
    store_id: int

class UpdateCartItemSchema(BaseModel):
    quantity: int = Field(ge=1)

class CartSchema(BaseModel):
    id: int
    user_id: int
    items: list[CartItemSchema]

class CreateOrderSchema(BaseModel):
    address_id: int


class OrderItemSchema(BaseModel):
    id: int
    order_id: int
    product: ProductSchema
    store_id: int
    quantity: int
    unit_price: float

class OrderSchema(BaseModel):
    id: int
    user_id: int
    address_id: int
    status: OrderStatus
    total_amount: float
    items: list[OrderItemSchema]
    created_at: datetime
    updated_at: datetime


class CreateOrderItemSchema(BaseModel):
    order_id: int
    product_id: int
    store_id: int
    quantity: int
    unit_price: float