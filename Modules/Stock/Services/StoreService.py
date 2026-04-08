from Modules.Stock.Repository.StoreRepository import IStoreRepository, get_store_repository
from Modules.Stock.Schemas import CreateStoreSchema, StoreSchema, UpdateStoreSchema
from Modules.Stock.Models import Store
from fastapi import HTTPException
from Core.Database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List


class StoreService:

    def __init__(self, store_repository: IStoreRepository):
        self.store_repository = store_repository

    def _serialize_store(self, store: Store) -> dict:
        return StoreSchema(
            id=store.id,
            name=store.name,
            address=store.address,
            created_at=store.created_at,
            updated_at=store.updated_at,
        ).model_dump(mode="json")

    def get_all_stores(self) -> List[dict]:
        stores = self.store_repository.get_all_stores()
        return [self._serialize_store(store) for store in stores]

    def get_store_by_id(self, store_id: int) -> dict:
        existing_store = self.store_repository.get_store_by_id(store_id)
        if not existing_store:
            raise HTTPException(status_code=404, detail="Store not found")
        return self._serialize_store(existing_store)

    def create_store(self, data: CreateStoreSchema) -> dict:
        new_store = Store(name=data.name, address=data.address)
        created_store = self.store_repository.create_store(new_store)
        return self._serialize_store(created_store)

    def update_store(self, store_id: int, data: UpdateStoreSchema) -> dict:
        existing_store = self.store_repository.get_store_by_id(store_id)
        if not existing_store:
            raise HTTPException(status_code=404, detail="Store not found")
        update_fields = data.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_fields.items():
            setattr(existing_store, field, value)
        updated_store = self.store_repository.update_store(existing_store)
        return self._serialize_store(updated_store)

    def delete_store(self, store_id: int) -> None:
        existing_store = self.store_repository.get_store_by_id(store_id)
        if not existing_store:
            raise HTTPException(status_code=404, detail="Store not found")
        self.store_repository.delete_store(existing_store)


def get_store_service(db: Session = Depends(get_db)) -> StoreService:
    return StoreService(get_store_repository(db))
