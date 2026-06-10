from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session
from Modules.Adresses.Models import Address
from Core.Database import get_db
from fastapi import Depends


class IAddressRepository(ABC):
    @abstractmethod

    def create_address(self, address: Address) -> Address:
        pass

    @abstractmethod
    def get_address_by_id(self, address_id: int) -> Address:
        pass

    @abstractmethod
    def get_addresses_by_user_id(self, user_id: int) -> List[Address]:
        pass

    @abstractmethod
    def update_address(self, address: Address) -> Address:
        pass

    @abstractmethod
    def delete_address(self, address: Address) -> None:
        pass



class AddressRepository(IAddressRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_address(self, address: Address) -> Address:
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address

    def get_address_by_id(self, address_id: int) -> Address:
        return self.db.query(Address).filter(Address.id == address_id).first()

    def get_addresses_by_user_id(self, user_id: int) -> List[Address]:
        return self.db.query(Address).filter(Address.user_id == user_id).all()

    def update_address(self, address: Address) -> Address:
        self.db.commit()
        self.db.refresh(address)
        return address

    def delete_address(self, address: Address) -> None:
        self.db.delete(address)
        self.db.commit()

def get_address_repository(db: Session = Depends(get_db)) -> IAddressRepository:
    return AddressRepository(db)