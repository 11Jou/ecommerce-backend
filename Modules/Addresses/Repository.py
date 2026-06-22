from abc import ABC, abstractmethod
from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Database.AsyncDatabase import get_db
from Modules.Addresses.Models import Address


class IAddressRepository(ABC):
    @abstractmethod
    async def create_address(self, address: Address) -> Address:
        pass

    @abstractmethod
    async def get_address_by_id(self, address_id: int) -> Address:
        pass

    @abstractmethod
    async def get_addresses_by_user_id(self, user_id: int) -> List[Address]:
        pass

    @abstractmethod
    async def update_address(self, address: Address) -> Address:
        pass

    @abstractmethod
    async def delete_address(self, address: Address) -> None:
        pass


class AddressRepository(IAddressRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_address(self, address: Address) -> Address:
        self.db.add(address)
        await self.db.commit()
        await self.db.refresh(address)
        return address

    async def get_address_by_id(self, address_id: int) -> Address:
        result = await self.db.execute(select(Address).where(Address.id == address_id))
        return result.scalars().first()

    async def get_addresses_by_user_id(self, user_id: int) -> List[Address]:
        result = await self.db.execute(select(Address).where(Address.user_id == user_id))
        return list(result.scalars().all())

    async def update_address(self, address: Address) -> Address:
        await self.db.commit()
        await self.db.refresh(address)
        return address

    async def delete_address(self, address: Address) -> None:
        await self.db.delete(address)
        await self.db.commit()


def get_address_repository(db: AsyncSession = Depends(get_db)) -> IAddressRepository:
    return AddressRepository(db)
