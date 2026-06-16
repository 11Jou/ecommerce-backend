from Modules.Payment.Models import Payment
from Modules.Payment.Schemas import PaymentSchema


def to_payment_schema(payment: Payment) -> PaymentSchema:
    return PaymentSchema(
        id=payment.id,
        order_id=payment.order_id,
        payment_method=payment.payment_method,
        provider=payment.provider,
        status=payment.status,
    )


def to_payment_dict(payment: Payment) -> dict:
    return to_payment_schema(payment).model_dump(mode="json")
