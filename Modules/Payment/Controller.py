from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Modules.Auth.CheckAuth import get_current_user
from Modules.Auth.Models import User
from Modules.Payment.Mapper import to_payment_dict
from Modules.Payment.Models import OnlineProvider
from Modules.Payment.Services import PaymentService, get_payment_service
from Utils.Response import success_response

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/pay/{order_id}")
async def pay_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends(get_payment_service),
) -> JSONResponse:
    payment = await payment_service.pay_order(current_user.id, order_id, OnlineProvider.STRIPE)
    return success_response(
        message="Payment completed successfully",
        data=to_payment_dict(payment),
        status_code=200,
    )
