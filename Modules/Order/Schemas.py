from datetime import datetime
from Modules.Order.Models import OrderStatus
from pydantic import BaseModel, conint, Field
from Modules.Stock.Schemas import ProductSchema, StoreSchema
from Modules.Addresses.Schemas import AddressSchema
from Modules.Payment.Models import PaymentMethod


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
    payment_method: PaymentMethod
    address_id: int


class OrderItemSchema(BaseModel):
    id: int
    product: ProductSchema
    store: StoreSchema
    quantity: int
    unit_price: float
    total_price: float

class OrderSchema(BaseModel):
    id: int
    address: AddressSchema
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