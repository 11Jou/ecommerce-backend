from abc import ABC, abstractmethod
from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Database.AsyncDatabase import get_db
from Modules.Stock.Models import Store


class IStoreRepository(ABC):
    @abstractmethod
    async def get_all_stores(self) -> List[Store]:
        pass

    @abstractmethod
    async def get_store_by_id(self, store_id: int) -> Store:
        pass

    @abstractmethod
    async def create_store(self, store: Store) -> Store:
        pass

    @abstractmethod
    async def update_store(self, store: Store) -> Store:
        pass

    @abstractmethod
    async def delete_store(self, store: Store) -> None:
        pass


class StoreRepository(IStoreRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_stores(self) -> List[Store]:
        result = await self.db.execute(select(Store))
        return list(result.scalars().all())

    async def get_store_by_id(self, store_id: int) -> Store:
        result = await self.db.execute(select(Store).where(Store.id == store_id))
        return result.scalars().first()

    async def create_store(self, store: Store) -> Store:
        self.db.add(store)
        await self.db.commit()
        await self.db.refresh(store)
        return store

    async def update_store(self, store: Store) -> Store:
        await self.db.commit()
        await self.db.refresh(store)
        return store

    async def delete_store(self, store: Store) -> None:
        await self.db.delete(store)
        await self.db.commit()


def get_store_repository(db: AsyncSession = Depends(get_db)) -> IStoreRepository:
    return StoreRepository(db)
