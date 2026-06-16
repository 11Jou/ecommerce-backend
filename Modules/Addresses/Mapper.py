from Modules.Addresses.Models import Address
from Modules.Addresses.Schemas import AddressSchema


def to_address_schema(address: Address) -> AddressSchema:
    return AddressSchema(
        id=address.id,
        user_id=address.user_id,
        city=address.city,
        street=address.street,
        building=address.building,
        additional_info=address.additional_info,
        created_at=address.created_at,
        updated_at=address.updated_at,
    )

def to_address_dict(address: Address) -> dict:
    return to_address_schema(address).model_dump(mode="json")