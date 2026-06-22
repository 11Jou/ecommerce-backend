from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Database.AsyncDatabase import get_db
from Modules.Stock.Models import Product
from Modules.Stock.Repository.ProductRepository import (
    IProductRepository,
    get_product_repository,
)
from Modules.Stock.Schemas import CreateProductSchema, UpdateProductSchema


class ProductService:
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    async def get_all_products(self) -> List[Product]:
        return await self.product_repository.get_all_products()

    async def get_active_products_with_availability(
        self, name: Optional[str] = None
    ) -> List[Product]:
        return await self.product_repository.get_active_products(name=name)

    async def get_product_by_id(self, product_id: int) -> Product:
        product = await self.product_repository.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    async def get_product_by_id_with_availability(self, product_id: int) -> Product:
        product = await self.product_repository.get_product_by_id(product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

    async def get_product_by_category(self, category_id: int) -> List[Product]:
        return await self.product_repository.get_product_by_category(category_id)

    async def create_product(self, product: CreateProductSchema) -> Product:
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            category_id=product.category_id,
            is_active=product.is_active,
        )
        return await self.product_repository.create_product(new_product)

    async def update_product(self, product_id: int, product: UpdateProductSchema) -> Product:
        existing_product = await self.product_repository.get_product_by_id(product_id)
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        update_data = product.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(existing_product, field, value)
        return await self.product_repository.update_product(existing_product)

    async def delete_product(self, product_id: int) -> None:
        existing_product = await self.product_repository.get_product_by_id(product_id)
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return await self.product_repository.delete_product(existing_product)


def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(product_repository=get_product_repository(db))
