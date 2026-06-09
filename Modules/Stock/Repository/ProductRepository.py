from abc import ABC, abstractmethod
from Modules.Stock.Models import Product, Stock
from typing import List, Optional
from Core.Database import get_db
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends

class IProductRepository(ABC):

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Product:
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
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .all()
        )

    def get_active_products(self, name: Optional[str] = None) -> List[Product]:
        query = (
            self.db.query(Product)
            .options(
                joinedload(Product.category),
                joinedload(Product.stocks).joinedload(Stock.store),
            )
            .filter(Product.is_active == True)
        )

        if name and name.strip():
            query = query.filter(Product.name.ilike(f"%{name.strip()}%"))

        return query.all()

    def get_product_by_id(self, product_id: int) -> Product:
        return (
            self.db.query(Product)
            .options(
                joinedload(Product.category),
                joinedload(Product.stocks).joinedload(Stock.store),
            )
            .filter(Product.id == product_id)
            .first()
        )

    def get_product_by_category(self, category_id: int) -> List[Product]:
        return (
            self.db.query(Product)
            .options(
                joinedload(Product.category),
                joinedload(Product.stocks).joinedload(Stock.store),
            )
            .filter(Product.category_id == category_id)
            .all()
        )

    def create_product(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_product(self, product: Product) -> Product:
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()
        return True

def get_product_repository(db: Session = Depends(get_db)) -> IProductRepository:
    return ProductRepository(db)