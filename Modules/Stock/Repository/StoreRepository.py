from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from Modules.Stock.Models import Store
from fastapi import Depends
from Core.Database import get_db
from typing import List


class IStoreRepository(ABC):

    @abstractmethod
    def get_store_by_id(self, store_id: int) -> Store:
        pass

    @abstractmethod
    def create_store(self, store: Store) -> Store:
        pass

    @abstractmethod
    def update_store(self, store: Store) -> Store:
        pass

    @abstractmethod
    def delete_store(self, store: Store) -> None:
        pass

class StoreRepository(IStoreRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all_stores(self) -> List[Store]:
        return self.db.query(Store).all()

    def get_store_by_id(self, store_id: int) -> Store:
        return self.db.query(Store).filter(Store.id == store_id).first()


    def create_store(self, store: Store) -> Store:
        self.db.add(store)
        self.db.commit()
        self.db.refresh(store)
        return store

    def update_store(self, store: Store) -> Store:
        self.db.commit()
        self.db.refresh(store)
        return store


    def delete_store(self, store: Store) -> None:
        self.db.delete(store)
        self.db.commit()
        return True

def get_store_repository(db: Session = Depends(get_db)) -> IStoreRepository:
    return StoreRepository(db)