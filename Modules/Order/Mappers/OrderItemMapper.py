from Modules.Order.Models import OrderItem
from Modules.Order.Schemas import OrderItemSchema
from Modules.Stock.Mappers.ProductMapper import to_product_schema

def to_order_item_schema(order_item: OrderItem) -> OrderItemSchema:
    return OrderItemSchema(
        id=order_item.id,
        order_id=order_item.order_id,
        product=to_product_schema(order_item.product),
        store_id=order_item.store_id,
        quantity=order_item.quantity,
        unit_price=float(order_item.unit_price),
        total_price=float(order_item.total_price),
    )

def to_order_item_dict(order_item: OrderItem) -> dict:
    return to_order_item_schema(order_item).model_dump(mode="json")