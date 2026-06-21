from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Database import get_db
from Modules.Order.Models import OrderStatus
from Modules.Order.Repository.OrderRepository import IOrderRepository, get_order_repository
from Modules.Payment.Gateways.Factory import OnlinePaymentGatewayFactory
from Modules.Payment.Models import Payment, PaymentMethod, PaymentStatus
from Modules.Payment.Repository import IPaymentRepository, get_payment_repository
from Modules.Payment.Schemas import PayOrderSchema


class PaymentService:
    def __init__(
        self,
        db: AsyncSession,
        payment_repository: IPaymentRepository,
        order_repository: IOrderRepository,
    ):
        self.db = db
        self.payment_repository = payment_repository
        self.order_repository = order_repository

    async def create_payment(self, payment: Payment) -> Payment:
        return await self.payment_repository.create_payment(payment)

    async def add_payment(self, payment: Payment) -> Payment:
        return await self.payment_repository.add_payment(payment)

    async def get_payment_by_id(self, payment_id: int) -> Payment:
        return await self.payment_repository.get_payment_by_id(payment_id)

    async def update_payment(self, payment: Payment) -> Payment:
        return await self.payment_repository.update_payment(payment)

    async def delete_payment(self, payment_id: int) -> None:
        return await self.payment_repository.delete_payment(payment_id)

    async def _claim_order_for_payment(self, order) -> None:
        if order.status != OrderStatus.PENDING_PAYMENT:
            raise HTTPException(status_code=400, detail="Order is not awaiting payment")
        order.status = OrderStatus.PAYMENT_PROCESSING
        await self.db.commit()

    async def _release_payment_claim(self, order, *, success: bool) -> None:
        if success:
            order.status = OrderStatus.PENDING_SHIPMENT
        else:
            order.status = OrderStatus.PENDING_PAYMENT
        await self.db.commit()

    async def pay_order(self, user_id: int, order_id: int, pay_data: PayOrderSchema) -> Payment:
        order = await self.order_repository.get_order_by_id(order_id, user_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        payment = await self.payment_repository.get_payment_by_order_id(order_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        if payment.payment_method != PaymentMethod.ONLINE_PAYMENT:
            raise HTTPException(status_code=400, detail="Order is not an online payment order")

        if payment.status != PaymentStatus.PENDING:
            raise HTTPException(status_code=400, detail="Payment has already been processed")

        await self._claim_order_for_payment(order)

        gateway = OnlinePaymentGatewayFactory.create(pay_data.online_provider)
        try:
            result = gateway.charge(float(order.total_amount), pay_data.card_details)

            if not result.success:
                payment.status = PaymentStatus.FAILED
                await self._release_payment_claim(order, success=False)
                raise HTTPException(status_code=400, detail="Online payment failed")

            payment.provider = pay_data.online_provider
            payment.status = PaymentStatus.COMPLETED
            await self._release_payment_claim(order, success=True)
            await self.db.refresh(payment)
        except HTTPException:
            raise
        except Exception:
            order.status = OrderStatus.PENDING_PAYMENT
            await self.db.commit()
            raise

        return payment


def get_payment_service(db: AsyncSession = Depends(get_db)) -> PaymentService:
    return PaymentService(
        db=db,
        payment_repository=get_payment_repository(db),
        order_repository=get_order_repository(db),
    )
