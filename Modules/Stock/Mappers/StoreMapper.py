from Modules.Stock.Models import Store
from Modules.Stock.Schemas import StoreSchema


def to_store_schema(store: Store) -> StoreSchema:
    return StoreSchema(
        id=store.id,
        name=store.name,
        address=store.address,
        created_at=store.created_at,
        updated_at=store.updated_at,
    )


def to_store_dict(store: Store) -> dict:
    return to_store_schema(store).model_dump(mode="json")
