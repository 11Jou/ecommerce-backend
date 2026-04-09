from Modules.Stock.Models import Product
from Modules.Stock.Schemas import (
    ProductSchema,
    ProductStoreAvailabilitySchema,
    ProductWithAvailabilitySchema,
)


def to_product_schema(product: Product) -> ProductSchema:
    return ProductSchema(
        id=product.id,
        name=product.name,
        description=product.description,
        price=float(product.price),
        category_id=product.category_id,
        is_active=product.is_active,
        created_at=product.created_at,
        updated_at=product.updated_at,
    )


def to_product_with_availability_schema(product: Product) -> ProductWithAvailabilitySchema:
    availability = [
        ProductStoreAvailabilitySchema(
            store_id=stock.store_id,
            store_name=stock.store.name if stock.store else "",
            quantity=stock.quantity,
        )
        for stock in product.stocks
    ]

    return ProductWithAvailabilitySchema(
        id=product.id,
        name=product.name,
        description=product.description,
        price=float(product.price),
        category_id=product.category_id,
        is_active=product.is_active,
        created_at=product.created_at,
        updated_at=product.updated_at,
        availability=availability,
    )


def to_product_dict(product: Product) -> dict:
    return to_product_schema(product).model_dump(mode="json")


def to_product_with_availability_dict(product: Product) -> dict:
    return to_product_with_availability_schema(product).model_dump(mode="json")
