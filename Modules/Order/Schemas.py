from datetime import datetime

from pydantic import BaseModel

from Modules.Addresses.Schemas import AddressSchema
from Modules.Order.Models import OrderStatus
from Modules.Payment.Models import PaymentMethod
from Modules.Stock.Schemas import ProductSchema, StoreSchema

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