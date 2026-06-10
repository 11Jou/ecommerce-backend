from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from Modules.Order.Services.CartService import CartService, get_cart_service
from Modules.Auth.CheckAuth import get_current_user
from Modules.Auth.Models import User
from Utils.Response import success_response
from Modules.Order.Schemas import *
from Modules.Order.Mappers.CartMapper import to_cart_dict

router = APIRouter(prefix="/order", tags=["order"])


@router.get("/cart")
def get_cart(
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
) -> JSONResponse:
    cart = cart_service.get_cart_by_user_id(current_user.id)
    return success_response(
        message="Cart retrieved successfully",
        data=to_cart_dict(cart),
        status_code=200,
    )


@router.post("/cart/add")
def add_item_to_cart(
    cart_item: CreateCartItemSchema,
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
) -> JSONResponse:
    cart = cart_service.get_cart_or_create(current_user.id)
    cart_service.create_cart_item(cart_item, cart.id)
    updated_cart = cart_service.get_cart_by_id(cart.id)
    return success_response(
        message="Item added to cart successfully",
        data=to_cart_dict(updated_cart),
        status_code=200,
    )

@router.put("/cart/items/{cart_item_id}")
def update_cart_item(
    cart_item_id: int,
    update_cart_item_schema: UpdateCartItemSchema,
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
) -> JSONResponse:
    cart = cart_service.get_cart_by_user_id(current_user.id)
    if not cart:
        return success_response(message="Cart not found", status_code=404)
    cart_service.update_item_quantity(cart_item_id=cart_item_id, quantity=update_cart_item_schema.quantity)
    updated_cart = cart_service.get_cart_by_id(cart.id)
    return success_response(
        message="Cart item updated successfully",
        data=to_cart_dict(updated_cart),
        status_code=200,
    )


@router.delete("/cart/items/{cart_item_id}")
def delete_cart_item(
    cart_item_id: int,
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
) -> JSONResponse:
    cart_service.remove_item_from_cart(cart_item_id)
    updated_cart = cart_service.get_cart_by_user_id(current_user.id)
    return success_response(
        message="Cart item deleted successfully",
        data=to_cart_dict(updated_cart),
        status_code=200,
    )


@router.delete("/cart/clear")
def clear_cart(
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
) -> JSONResponse:
    cart = cart_service.get_cart_by_user_id(current_user.id)
    cart_service.clear_cart(cart.id)
    updated_cart = cart_service.get_cart_by_user_id(current_user.id)
    return success_response(
        message="Cart cleared successfully",
        data=to_cart_dict(updated_cart),
        status_code=200,
    )
