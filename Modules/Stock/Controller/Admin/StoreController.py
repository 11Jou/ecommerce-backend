from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Modules.Auth.CheckAuth import require_role
from Modules.Auth.Models import User
from Modules.Stock.Mappers.StoreMapper import to_store_dict
from Modules.Stock.Schemas import CreateStoreSchema, UpdateStoreSchema
from Modules.Stock.Services.StoreService import StoreService, get_store_service
from Utils.Response import success_response

router = APIRouter(tags=["stock/admin/stores"])


@router.get("/stores")
async def get_all_stores_controller(
    current_user: User = Depends(require_role(["admin"])),
    store_service: StoreService = Depends(get_store_service),
) -> JSONResponse:
    stores = await store_service.get_all_stores()
    return success_response(
        message="Stores fetched successfully",
        data=[to_store_dict(store) for store in stores],
        status_code=200,
    )


@router.post("/stores")
async def create_store_controller(
    store_data: CreateStoreSchema,
    current_user: User = Depends(require_role(["admin"])),
    store_service: StoreService = Depends(get_store_service),
) -> JSONResponse:
    store = await store_service.create_store(store_data)
    return success_response(
        message="Store created successfully",
        data=to_store_dict(store),
        status_code=201,
    )


@router.put("/stores/{store_id}")
async def update_store_controller(
    store_id: int,
    store_data: UpdateStoreSchema,
    current_user: User = Depends(require_role(["admin"])),
    store_service: StoreService = Depends(get_store_service),
) -> JSONResponse:
    store = await store_service.update_store(store_id, store_data)
    return success_response(
        message="Store updated successfully",
        data=to_store_dict(store),
        status_code=200,
    )


@router.delete("/stores/{store_id}")
async def delete_store_controller(
    store_id: int,
    current_user: User = Depends(require_role(["admin"])),
    store_service: StoreService = Depends(get_store_service),
) -> JSONResponse:
    await store_service.delete_store(store_id)
    return success_response(message="Store deleted successfully", status_code=200)
