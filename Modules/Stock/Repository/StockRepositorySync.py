from sqlalchemy import select
from sqlalchemy.orm import Session

from Modules.Stock.Models import Stock


class StockRepositorySync:
    def __init__(self, db: Session):
        self.db = db

    def get_stock_by_product_id_and_store_id(self, product_id: int, store_id: int) -> Stock | None:
        result = self.db.execute(
            select(Stock).where(Stock.product_id == product_id, Stock.store_id == store_id)
        )
        return result.scalars().first()

    def release_stock(self, product_id: int, store_id: int, quantity: int) -> Stock:
        stock = self.get_stock_by_product_id_and_store_id(product_id, store_id)
        if not stock:
            raise ValueError(f"Stock not found for product {product_id} and store {store_id}")
        stock.quantity += quantity
        return stock
