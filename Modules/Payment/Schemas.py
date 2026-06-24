from typing import Optional
from pydantic import BaseModel
from Modules.Payment.Models import PaymentMethod, OnlineProvider, PaymentStatus



class PayOrderSchema(BaseModel):
    online_provider: OnlineProvider


class PaymentSchema(BaseModel):
    id: int
    order_id: int
    payment_method: PaymentMethod
    provider: Optional[OnlineProvider] = None
    status: PaymentStatus
