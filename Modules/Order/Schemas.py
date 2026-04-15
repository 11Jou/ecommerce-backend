from datetime import datetime
from Modules.Order.Models import OrderStatus
from pydantic import BaseModel

class CreateOrderSchema(BaseModel):
    user_id: int
    address_id: int
    status: OrderStatus

class OrderSchema(BaseModel):
    id: int
    user_id: int
    address_id: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime


class CreateOrderItemSchema(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float

class OrderItemSchema(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float
    created_at: datetime
    updated_at: datetime