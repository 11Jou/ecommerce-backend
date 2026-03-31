from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Generic, TypeVar
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

T = TypeVar("T")


def _json_safe(value: Any) -> Any:
    """Make nested structures JSON-serializable (e.g. Pydantic error ``ctx`` may contain exceptions)."""
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, BaseException):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(v) for v in value]
    try:
        return jsonable_encoder(value)
    except Exception:
        return str(value)


class ApiResponse(BaseModel, Generic[T]):
    """Standard API envelope for success and error responses."""

    success: bool
    message: str
    data: T | None = None
    error: Any | None = None
    status_code: int = Field(
        ...,
        description="Same as HTTP status; duplicated in body for clients that only read JSON.",
    )

    model_config = {"arbitrary_types_allowed": True}


def success_response(
    *,
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
) -> JSONResponse:
    payload = ApiResponse[Any](
        success=True,
        message=message,
        data=_json_safe(data),
        error=None,
        status_code=status_code,
    )
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(payload.model_dump(mode="json")),
    )


def failed_response(
    *,
    message: str,
    error: Any = None,
    data: Any = None,
    status_code: int = 400,
) -> JSONResponse:
    payload = ApiResponse[Any](
        success=False,
        message=message,
        data=_json_safe(data),
        error=_json_safe(error),
        status_code=status_code,
    )
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(payload.model_dump(mode="json")),
    )
