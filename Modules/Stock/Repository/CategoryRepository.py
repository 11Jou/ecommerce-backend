from abc import ABC, abstractmethod
from Modules.Stock.Models import Category
from Core.Database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List


class ICategoryRepository(ABC):

    @abstractmethod
    def get_all_categories(self) -> List[Category]:
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> Category:
        pass

    @abstractmethod
    def create_category(self, category: Category) -> Category:
        pass

    @abstractmethod
    def update_category(self, category: Category) -> Category:
        pass

    @abstractmethod
    def delete_category(self, category_id: int) -> None:
        pass


class CategoryRepository(ICategoryRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all_categories(self) -> List[Category]:
        return self.db.query(Category).all()

    def get_category_by_id(self, category_id: int) -> Category:
        return self.db.query(Category).filter(Category.id == category_id).first()

    def create_category(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update_category(self, category: Category) -> Category:
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete_category(self, category_id: int) -> None:
        category = self.get_category_by_id(category_id)
        if category:
            self.db.delete(category)
            self.db.commit()


def get_category_repository(db: Session = Depends(get_db)) -> ICategoryRepository:
    return CategoryRepository(db)
