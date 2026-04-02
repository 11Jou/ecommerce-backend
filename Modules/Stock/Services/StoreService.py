from Modules.Stock.Repository.StoreRepository import IStoreRepository, get_store_repository
from Modules.Stock.Schemas import CreateStoreSchema, UpdateStoreSchema
from Modules.Stock.Models import Store
from fastapi import HTTPException
from Core.Database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List


class StoreService:

    def __init__(self, store_repository: IStoreRepository):
        self.store_repository = store_repository

    def get_all_stores(self) -> List[Store]:
        return self.store_repository.get_all_stores()

    def get_store_by_id(self, store_id: int) -> Store:
        return self.store_repository.get_store_by_id(store_id)

    def create_store(self, data: CreateStoreSchema) -> Store:
        new_store = Store(name=data.name, address=data.address)
        return self.store_repository.create_store(new_store)

    def update_store(self, store_id: int, data: UpdateStoreSchema) -> Store:
        existing_store = self.get_store_by_id(store_id)
        if not existing_store:
            raise HTTPException(status_code=404, detail="Store not found")
        update_fields = data.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_fields.items():
            setattr(existing_store, field, value)
        return self.store_repository.update_store(existing_store)

    def delete_store(self, store_id: int) -> None:
        existing_store = self.get_store_by_id(store_id)
        if not existing_store:
            raise HTTPException(status_code=404, detail="Store not found")
        self.store_repository.delete_store(existing_store)


def get_store_service(db: Session = Depends(get_db)) -> StoreService:
    return StoreService(get_store_repository(db))
