from typing import List
from Modules.Stock.Repository.ProductRepository import IProductRepository, ProductRepository, get_product_repository
from Modules.Stock.Schemas import CreateProductSchema, UpdateProductSchema
from Modules.Stock.Models import Product
from fastapi import HTTPException
from Core.Database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

class ProductService:
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    def get_all_products(self) -> List[Product]:
        return self.product_repository.get_all_products()

    def get_active_products(self) -> List[Product]:
        return self.product_repository.get_active_products()

    def get_product_by_id(self, product_id: int) -> Product:
        return self.product_repository.get_product_by_id(product_id)

    def get_product_by_name(self, name: str) -> List[Product]:
        return self.product_repository.get_product_by_name(name)

    def get_product_by_category(self, category_id: int) -> List[Product]:
        return self.product_repository.get_product_by_category(category_id)

    def create_product(self, product: CreateProductSchema) -> Product:
        new_product = Product(name=product.name, description=product.description, price=product.price, category_id=product.category_id, is_active=product.is_active)
        return self.product_repository.create_product(new_product)

    def update_product(self, product_id: int, product: UpdateProductSchema) -> Product:
        existing_product = self.get_product_by_id(product_id)
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        update_data = product.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(existing_product, field, value)
        return self.product_repository.update_product(existing_product)
    
    def delete_product(self, product_id: int) -> None:
        existing_product = self.get_product_by_id(product_id)
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return self.product_repository.delete_product(existing_product)

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(product_repository=get_product_repository(db))

