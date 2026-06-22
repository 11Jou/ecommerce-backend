from Modules.Order.Models import Order
from Modules.Order.Schemas import OrderSchema
from Modules.Order.Mappers.OrderItemMapper import to_order_item_dict
from Modules.Addresses.Mapper import to_address_dict

def to_order_schema(order: Order) -> OrderSchema:
    return OrderSchema(
        id=order.id,
        user_id=order.user_id,
        address=to_address_dict(order.address),
        items=[to_order_item_dict(item) for item in order.items],
        status=order.status,
        total_amount=float(order.total_amount),
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


def to_order_dict(order: Order) -> dict:
    return to_order_schema(order).model_dump(mode="json")