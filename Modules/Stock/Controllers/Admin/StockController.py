from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Modules.Auth.CheckAuth import require_role
from Modules.Auth.Models import User
from Modules.Stock.Mappers.StockMapper import to_stock_dict
from Modules.Stock.Schemas import CreateStockSchema, UpdateStockSchema
from Modules.Stock.Services.StockService import StockService, get_stock_service
from Utils.Response import success_response

router = APIRouter(tags=["stock/admin/stocks"])


@router.get("/stocks")
async def get_all_stocks_controller(
    current_user: User = Depends(require_role(["admin"])),
    stock_service: StockService = Depends(get_stock_service),
) -> JSONResponse:
    stocks = await stock_service.get_all_stocks()
    return success_response(
        message="Stocks fetched successfully",
        data=[to_stock_dict(stock) for stock in stocks],
        status_code=200,
    )


@router.get("/stocks/store/{store_id}/product/{product_id}")
async def get_stock_by_store_and_product_controller(
    store_id: int,
    product_id: int,
    current_user: User = Depends(require_role(["admin"])),
    stock_service: StockService = Depends(get_stock_service),
) -> JSONResponse:
    stock = await stock_service.get_stock_by_product_id_and_store_id(product_id, store_id)
    return success_response(
        message="Stock fetched successfully",
        data=to_stock_dict(stock),
        status_code=200,
    )


@router.get("/stocks/product/{product_id}")
async def get_stocks_by_product_id_controller(
    product_id: int,
    current_user: User = Depends(require_role(["admin"])),
    stock_service: StockService = Depends(get_stock_service),
) -> JSONResponse:
    stocks = await stock_service.get_stocks_by_product_id(product_id)
    return success_response(
        message="Stocks fetched successfully",
        data=[to_stock_dict(stock) for stock in stocks],
        status_code=200,
    )


@router.get("/stocks/store/{store_id}")
async def get_stocks_by_store_id_controller(
    store_id: int,
    current_user: User = Depends(require_role(["admin"])),
    stock_service: StockService = Depends(get_stock_service),
) -> JSONResponse:
    stocks = await stock_service.get_stocks_by_store_id(store_id)
    return success_response(
        message="Stocks fetched successfully",
        data=[to_stock_dict(stock) for stock in stocks],
        status_code=200,
    )


@router.post("/stocks")
async def create_stock_controller(
    stock_data: CreateStockSchema,
    current_user: User = Depends(require_role(["admin"])),
    stock_service: StockService = Depends(get_stock_service),
) -> JSONResponse:
    stock = await stock_service.create_stock(stock_data)
    return success_response(
        message="Stock created successfully",
        data=to_stock_dict(stock),
        status_code=201,
    )


@router.put("/stocks/store/{store_id}/product/{product_id}")
async def update_stock_controller(
    store_id: int,
    product_id: int,
    stock_data: UpdateStockSchema,
    current_user: User = Depends(require_role(["admin"])),
    stock_service: StockService = Depends(get_stock_service),
) -> JSONResponse:
    stock = await stock_service.update_stock(store_id, product_id, stock_data)
    return success_response(
        message="Stock updated successfully",
        data=to_stock_dict(stock),
        status_code=200,
    )


@router.delete("/stocks/store/{store_id}/product/{product_id}")
async def delete_stock_controller(
    store_id: int,
    product_id: int,
    current_user: User = Depends(require_role(["admin"])),
    stock_service: StockService = Depends(get_stock_service),
) -> JSONResponse:
    await stock_service.delete_stock(store_id, product_id)
    return success_response(message="Stock deleted successfully", status_code=200)
