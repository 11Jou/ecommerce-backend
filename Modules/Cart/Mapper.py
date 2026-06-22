from Modules.Cart.Models import Cart, CartItem
from Modules.Cart.Schemas import CartItemSchema, CartSchema
from Modules.Stock.Mappers.ProductMapper import to_product_schema


def to_cart_item_schema(cart_item: CartItem) -> CartItemSchema:
    return CartItemSchema(
        id=cart_item.id,
        product=to_product_schema(cart_item.product),
        quantity=cart_item.quantity,
        store_id=cart_item.store_id,
    )


def to_cart_item_dict(cart_item: CartItem) -> dict:
    return to_cart_item_schema(cart_item).model_dump(mode="json")


def to_cart_schema(cart: Cart) -> CartSchema:
    return CartSchema(
        id=cart.id,
        user_id=cart.user_id,
        items=[to_cart_item_schema(item) for item in cart.items],
    )


def to_cart_dict(cart: Cart) -> dict:
    return to_cart_schema(cart).model_dump(mode="json")
