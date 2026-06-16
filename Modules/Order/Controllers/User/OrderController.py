from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from Modules.Order.Services.OrderService import OrderService, get_order_service
from Modules.Auth.CheckAuth import get_current_user
from Modules.Auth.Models import User
from Utils.Response import success_response
from Modules.Order.Schemas import *
from Modules.Order.Mappers.OrderMapper import to_order_dict

router = APIRouter(prefix="/order", tags=["order"])



@router.get("/")
def get_orders(
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
) -> JSONResponse:
    orders = order_service.get_orders_by_user_id(current_user.id)
    return success_response(
        message="Orders retrieved successfully",
        data=[to_order_dict(order) for order in orders],
        status_code=200,
    )



@router.get("/{order_id}")
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
) -> JSONResponse:
    order = order_service.get_order_by_id(order_id, current_user.id)
    return success_response(
        message="Order retrieved successfully",
        data=to_order_dict(order),
        status_code=200,
    )


    

@router.post("/place-order")
def create_order(
    create_order_schema: CreateOrderSchema,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
) -> JSONResponse:
    order = order_service.place_order(current_user.id, create_order_schema)
    return success_response(
        message="Order created successfully",
        data=to_order_dict(order),
        status_code=200,
    )

