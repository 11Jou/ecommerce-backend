from Modules.Stock.Models import Category
from Modules.Stock.Schemas import CategorySchema


def to_category_schema(category: Category) -> CategorySchema:
    return CategorySchema(
        id=category.id,
        name=category.name,
        description=category.description,
        is_active=category.is_active,
        created_at=category.created_at,
        updated_at=category.updated_at,
    )


def to_category_dict(category: Category) -> dict:
    return to_category_schema(category).model_dump(mode="json")
