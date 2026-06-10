from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from Modules.Adresses.Services import AdressesService, get_adresses_service
from Modules.Adresses.Schemas import CreateAddressSchema, UpdateAddressSchema
from Modules.Auth.CheckAuth import get_current_user
from Modules.Auth.Models import User
from Utils.Response import success_response
from Modules.Adresses.Mapper import to_address_schema, to_address_dict


router = APIRouter(prefix="/addresses", tags=["addresses"])



@router.get("/")
def get_addresses(
    current_user: User = Depends(get_current_user),
    adresses_service: AdressesService = Depends(get_adresses_service),
) -> JSONResponse:
    addresses = adresses_service.get_addresses_by_user_id(current_user.id)
    return success_response(
        message="Addresses retrieved successfully",
        data=[to_address_dict(address) for address in addresses],
        status_code=200,
    )

@router.get("/{address_id}")
def get_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    adresses_service: AdressesService = Depends(get_adresses_service),
) -> JSONResponse:
    address = adresses_service.get_address_by_id(address_id)



@router.post("/")
def create_address(
    create_address_schema: CreateAddressSchema,
    current_user: User = Depends(get_current_user),
    adresses_service: AdressesService = Depends(get_adresses_service),
) -> JSONResponse:
    address = adresses_service.create_address(current_user.id, create_address_schema)
    return success_response(
        message="Address created successfully",
        data=to_address_dict(address),
        status_code=201,
    )


@router.put("/{address_id}")
def update_address(
    address_id: int,
    update_address_schema: UpdateAddressSchema,
    current_user: User = Depends(get_current_user),
    adresses_service: AdressesService = Depends(get_adresses_service),
) -> JSONResponse:
    address = adresses_service.update_address(address_id, update_address_schema)
    return success_response(
        message="Address updated successfully",
        data=to_address_dict(address),
        status_code=200,
    )



@router.delete("/{address_id}")
def delete_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    adresses_service: AdressesService = Depends(get_adresses_service),
) -> JSONResponse:
    adresses_service.delete_address(address_id)
    return success_response(
        message="Address deleted successfully",
        status_code=200,
    )