from Modules.Stock.Models import Stock
from Modules.Stock.Schemas import StockSchema


def to_stock_schema(stock: Stock) -> StockSchema:
    return StockSchema(
        store_id=stock.store_id,
        product_id=stock.product_id,
        quantity=stock.quantity,
        created_at=stock.created_at,
        updated_at=stock.updated_at,
    )


def to_stock_dict(stock: Stock) -> dict:
    return to_stock_schema(stock).model_dump(mode="json")
