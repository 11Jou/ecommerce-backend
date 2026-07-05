from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Modules.Addresses.Mapper import to_address_dict
from Modules.Addresses.Schemas import CreateAddressSchema, UpdateAddressSchema
from Modules.Addresses.Services import AddressesService, get_addresses_service
from Modules.Auth.CheckAuth import get_current_verified_user
from Modules.Auth.Models import User
from Utils.Pagination import PaginationParams, build_pagination_meta
from Utils.Response import success_response

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.get("/")
async def get_addresses(
    current_user: User = Depends(get_current_verified_user),
    addresses_service: AddressesService = Depends(get_addresses_service),
    pagination: PaginationParams = Depends(),
) -> JSONResponse:
    result = await addresses_service.get_addresses_by_user_id(
        current_user.id, pagination.page, pagination.page_size
    )
    return success_response(
        message="Addresses retrieved successfully",
        data=[to_address_dict(address) for address in result.items],
        pagination=build_pagination_meta(pagination.page, pagination.page_size, result.total),
        status_code=200,
    )


@router.get("/{address_id}")
async def get_address(
    address_id: int,
    current_user: User = Depends(get_current_verified_user),
    addresses_service: AddressesService = Depends(get_addresses_service),
) -> JSONResponse:
    address = await addresses_service.get_address_by_id(current_user.id, address_id)
    return success_response(
        message="Address retrieved successfully",
        data=to_address_dict(address),
        status_code=200,
    )


@router.post("/")
async def create_address(
    create_address_schema: CreateAddressSchema,
    current_user: User = Depends(get_current_verified_user),
    addresses_service: AddressesService = Depends(get_addresses_service),
) -> JSONResponse:
    address = await addresses_service.create_address(current_user.id, create_address_schema)
    return success_response(
        message="Address created successfully",
        data=to_address_dict(address),
        status_code=201,
    )


@router.put("/{address_id}")
async def update_address(
    address_id: int,
    update_address_schema: UpdateAddressSchema,
    current_user: User = Depends(get_current_verified_user),
    addresses_service: AddressesService = Depends(get_addresses_service),
) -> JSONResponse:
    address = await addresses_service.update_address(
        current_user.id, address_id, update_address_schema
    )
    return success_response(
        message="Address updated successfully",
        data=to_address_dict(address),
        status_code=200,
    )
