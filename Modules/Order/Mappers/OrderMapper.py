from Modules.Order.Models import Order
from Modules.Order.Schemas import OrderSchema

def to_order_schema(order: Order) -> OrderSchema:
    return OrderSchema(
        id=order.id,
        user_id=order.user_id,
        address_id=order.address_id,
        status=order.status,
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


def to_order_dict(order: Order) -> dict:
    return to_order_schema(order).model_dump(mode="json")