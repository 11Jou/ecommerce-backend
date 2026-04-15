from Modules.Order.Models import OrderItem
from Modules.Order.Schemas import OrderItemSchema

def to_order_item_schema(order_item: OrderItem) -> OrderItemSchema:
    return OrderItemSchema(
        id=order_item.id,
        order_id=order_item.order_id,
        product_id=order_item.product_id,
        quantity=order_item.quantity,
        price=order_item.price,
        created_at=order_item.created_at,
        updated_at=order_item.updated_at,
    )

def to_order_item_dict(order_item: OrderItem) -> dict:
    return to_order_item_schema(order_item).model_dump(mode="json")