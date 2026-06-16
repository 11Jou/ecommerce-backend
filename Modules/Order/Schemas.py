from datetime import datetime
from typing import Optional
from Modules.Order.Models import OrderStatus
from pydantic import BaseModel, conint, Field, model_validator
from Modules.Stock.Schemas import ProductSchema, StoreSchema
from Modules.Addresses.Schemas import AddressSchema
from Modules.Payment.Models import PaymentMethod, OnlineProvider


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

class CardDetailsSchema(BaseModel):
    card_number: str
    cvc: str


class CreateOrderSchema(BaseModel):
    payment_method: PaymentMethod
    address_id: int
    online_provider: Optional[OnlineProvider] = None
    card_details: Optional[CardDetailsSchema] = None

    @model_validator(mode="after")
    def validate_payment_method(self):
        if self.payment_method == PaymentMethod.ONLINE_PAYMENT:
            if self.online_provider is None or self.card_details is None:
                raise ValueError(
                    "online_provider and card_details are required for online payment"
                )
        else:
            if self.online_provider is not None or self.card_details is not None:
                raise ValueError(
                    "online_provider and card_details must be omitted for this payment method"
                )
        return self


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