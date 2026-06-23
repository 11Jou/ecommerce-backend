from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
    ):
        self.page = page
        self.page_size = page_size


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool


@dataclass
class PaginatedResult(Generic[T]):
    items: list[T]
    total: int


def build_pagination_meta(page: int, page_size: int, total_items: int) -> PaginationMeta:
    total_pages = ceil(total_items / page_size) if total_items > 0 else 0
    return PaginationMeta(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1,
    )


def paginate(stmt: Select, page: int, page_size: int) -> Select:
    offset = (page - 1) * page_size
    return stmt.offset(offset).limit(page_size)


async def count_total(db: AsyncSession, stmt: Select) -> int:
    descriptions = stmt.column_descriptions
    if descriptions and descriptions[0].get("entity") is not None:
        model = descriptions[0]["entity"]
        count_stmt = select(func.count()).select_from(model)
        if stmt.whereclause is not None:
            count_stmt = count_stmt.where(stmt.whereclause)
        result = await db.execute(count_stmt)
        return result.scalar_one()

    count_stmt = select(func.count()).select_from(
        stmt.order_by(None).limit(None).offset(None).subquery()
    )
    result = await db.execute(count_stmt)
    return result.scalar_one()
