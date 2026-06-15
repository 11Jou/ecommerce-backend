from typing import List
from sqlalchemy.orm import Session
from Modules.Adresses.Models import Address
from Modules.Adresses.Repository import IAddressRepository, get_address_repository
from Modules.Adresses.Schemas import CreateAddressSchema, UpdateAddressSchema
from Core.Database import get_db
from fastapi import HTTPException
from fastapi import Depends

class AdressesService:

    def __init__(self, address_repository: IAddressRepository):
        self.address_repository = address_repository

    def create_address(self, user_id: int, create_address_schema: CreateAddressSchema) -> Address:
        address = Address(
            user_id=user_id,
            city=create_address_schema.city,
            street=create_address_schema.street,
            building=create_address_schema.building,
            additional_info=create_address_schema.additional_info,
        )
        return self.address_repository.create_address(address)

    def validate_user_address(self, user_id: int, address: Address) -> None:
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        if address.user_id != user_id:
            raise HTTPException(status_code=403, detail="Address does not belong to user")

    def get_address_by_id(self, user_id: int, address_id: int) -> Address:
        address = self.address_repository.get_address_by_id(address_id)

        self.validate_user_address(user_id, address)
        return address

    def get_addresses_by_user_id(self, user_id: int) -> List[Address]:
        return self.address_repository.get_addresses_by_user_id(user_id)


    def update_address(self, user_id: int, address_id: int, update_address_schema: UpdateAddressSchema) -> Address:
        address = self.address_repository.get_address_by_id(address_id)
        self.validate_user_address(user_id, address)
        update_data = update_address_schema.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(address, field, value)
        return self.address_repository.update_address(address)

    def delete_address(self, user_id: int, address_id: int) -> None:
        address = self.address_repository.get_address_by_id(address_id)
        self.validate_user_address(user_id, address)
        return self.address_repository.delete_address(address)

def get_adresses_service(db: Session = Depends(get_db)) -> AdressesService:
    return AdressesService(get_address_repository(db))