from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Modules.Auth.CheckAuth import require_role
from Modules.Auth.Models import User
from Modules.Order.Mappers.OrderMapper import to_order_dict
from Modules.Order.Services.OrderService import OrderService, get_order_service
from Utils.Response import success_response

router = APIRouter(prefix="/admin/order", tags=["admin/order"])


@router.get("/")
async def get_all_orders(
    current_user: User = Depends(require_role(["admin"])),
    order_service: OrderService = Depends(get_order_service),
) -> JSONResponse:
    orders = await order_service.get_all_orders()
    return success_response(
        message="All orders fetched successfully",
        data=[to_order_dict(order) for order in orders],
        status_code=200,
    )