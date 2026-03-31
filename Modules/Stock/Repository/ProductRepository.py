from abc import ABC, abstractmethod
from Modules.Stock.Models import Product
from typing import List
from Core.Database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

class IProductRepository(ABC):

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Product:
        pass

    @abstractmethod
    def get_product_by_name(self, name: str) -> List[Product]:
        pass

    def get_product_by_category(self, category_id: int) -> List[Product]:
        pass

    @abstractmethod
    def create_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    def update_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> None:
        pass



class ProductRepository(IProductRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all_products(self) -> List[Product]:
        return self.db.query(Product).all()

    def get_product_by_id(self, product_id: int) -> Product:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_product_by_name(self, name: str) -> List[Product]:
        return self.db.query(Product).filter(Product.name == name).all()

    def get_product_by_category(self, category_id: int) -> List[Product]:
        return self.db.query(Product).filter(Product.category_id == category_id).all()

    def create_product(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_product(self, product: Product) -> Product:
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: int) -> None:
        product = self.get_product_by_id(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False

def get_product_repository(db: Session = Depends(get_db)) -> IProductRepository:
    return ProductRepository(db)