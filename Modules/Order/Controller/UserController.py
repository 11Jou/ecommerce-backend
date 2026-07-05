from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Modules.Auth.CheckAuth import get_current_verified_user
from Modules.Auth.Models import User
from Modules.Order.Mappers.OrderMapper import to_order_dict
from Modules.Order.Schemas import CreateOrderSchema
from Modules.Order.Services.OrderService import OrderService, get_order_service
from Utils.Pagination import PaginationParams, build_pagination_meta
from Utils.Response import success_response

router = APIRouter(prefix="/order", tags=["order"])


@router.get("/")
async def get_orders(
    current_user: User = Depends(get_current_verified_user),
    order_service: OrderService = Depends(get_order_service),
    pagination: PaginationParams = Depends(),
) -> JSONResponse:
    result = await order_service.get_orders_by_user_id(
        current_user.id, pagination.page, pagination.page_size
    )
    return success_response(
        message="Orders retrieved successfully",
        data=[to_order_dict(order) for order in result.items],
        pagination=build_pagination_meta(pagination.page, pagination.page_size, result.total),
        status_code=200,
    )


@router.get("/{order_id}")
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_verified_user),
    order_service: OrderService = Depends(get_order_service),
) -> JSONResponse:
    order = await order_service.get_order_by_id(order_id, current_user.id)
    return success_response(
        message="Order retrieved successfully",
        data=to_order_dict(order),
        status_code=200,
    )


@router.post("/place-order")
async def create_order(
    create_order_schema: CreateOrderSchema,
    current_user: User = Depends(get_current_verified_user),
    order_service: OrderService = Depends(get_order_service),
) -> JSONResponse:
    order = await order_service.place_order(current_user.id, create_order_schema)
    return success_response(
        message="Order created successfully",
        status_code=200,
    )
