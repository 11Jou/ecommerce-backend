from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Modules.Auth.CheckAuth import require_role
from Modules.Auth.Models import User
from Modules.Order.Mappers.OrderMapper import to_order_dict
from Modules.Order.Services.OrderService import OrderService, get_order_service
from Utils.Pagination import PaginationParams, build_pagination_meta
from Utils.Response import success_response

router = APIRouter(prefix="/admin/order", tags=["admin/order"])


@router.get("/")
async def get_all_orders(
    current_user: User = Depends(require_role(["admin"])),
    order_service: OrderService = Depends(get_order_service),
    pagination: PaginationParams = Depends(),
) -> JSONResponse:
    result = await order_service.get_all_orders(pagination.page, pagination.page_size)
    return success_response(
        message="All orders fetched successfully",
        data=[to_order_dict(order) for order in result.items],
        pagination=build_pagination_meta(pagination.page, pagination.page_size, result.total),
        status_code=200,
    )