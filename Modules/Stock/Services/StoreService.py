class StoreService:

    def __init__(self, store_repository: IStoreRepository):
        self.store_repository = store_repository

    def get_store_by_id(self, store_id: int) -> Store:
        return self.store_repository.get_store_by_id(store_id)

    def create_store(self, store: Store) -> Store:
        new_store = Store(
            name=store.name,
            address=store.address)

        return self.store_repository.create_store(new_store)

    def update_store(self, store: Store) -> Store:
        existing_store = self.get_store_by_id(store.id)
        if not existing_store:
            raise HTTPException(status_code=404, detail="Store not found")
        update_data = store.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(existing_store, field, value)
        return self.store_repository.update_store(existing_store)

    def delete_store(self, store_id: int) -> None:
        existing_store = self.get_store_by_id(store_id)
        if not existing_store:
            raise HTTPException(status_code=404, detail="Store not found")
        return self.store_repository.delete_store(existing_store)
