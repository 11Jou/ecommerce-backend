from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Database import get_db
from Modules.Addresses.Models import Address
from Modules.Addresses.Repository import IAddressRepository, get_address_repository
from Modules.Addresses.Schemas import CreateAddressSchema, UpdateAddressSchema
from Modules.Order.Repository.OrderRepository import IOrderRepository, get_order_repository


class AddressesService:
    def __init__(self, address_repository: IAddressRepository, order_repository: IOrderRepository):
        self.address_repository = address_repository
        self.order_repository = order_repository

    async def create_address(self, user_id: int, create_address_schema: CreateAddressSchema) -> Address:
        address = Address(
            user_id=user_id,
            city=create_address_schema.city,
            street=create_address_schema.street,
            building=create_address_schema.building,
            additional_info=create_address_schema.additional_info,
        )
        return await self.address_repository.create_address(address)

    def validate_user_address(self, user_id: int, address: Address) -> None:
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        if address.user_id != user_id:
            raise HTTPException(status_code=403, detail="Address does not belong to user")

    async def get_address_by_id(self, user_id: int, address_id: int) -> Address:
        return await self.address_repository.get_address_by_id(address_id)

    async def get_addresses_by_user_id(self, user_id: int) -> List[Address]:
        return await self.address_repository.get_addresses_by_user_id(user_id)

    async def update_address(
        self, user_id: int, address_id: int, update_address_schema: UpdateAddressSchema
    ) -> Address:
        address = await self.address_repository.get_address_by_id(address_id)
        self.validate_user_address(user_id, address)
        update_data = update_address_schema.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(address, field, value)
        return await self.address_repository.update_address(address)


def get_addresses_service(db: AsyncSession = Depends(get_db)) -> AddressesService:
    return AddressesService(get_address_repository(db), get_order_repository(db))
