from typing import Optional

from pydantic import BaseModel

from Modules.Payment.Models import PaymentMethod, OnlineProvider, PaymentStatus


class CardDetailsSchema(BaseModel):
    card_number: str
    cvc: str


class PayOrderSchema(BaseModel):
    online_provider: OnlineProvider
    card_details: CardDetailsSchema


class PaymentSchema(BaseModel):
    id: int
    order_id: int
    payment_method: PaymentMethod
    provider: Optional[OnlineProvider] = None
    status: PaymentStatus
