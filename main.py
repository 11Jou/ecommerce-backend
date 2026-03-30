from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError

from Modules.Auth.Controller import router as AuthRouter
from Modules.Stock.Controllers import UserRouter as StockUserRouter, AdminRouter as StockAdminRouter
from Modules.UserProfile.Controller import router as UserProfileRouter
from Utils.Response import failed_response


def _http_message(detail: object) -> str:
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list):
        return "Request failed"
    return "Request failed"


app = FastAPI()

app.include_router(AuthRouter)
app.include_router(UserProfileRouter)
app.include_router(StockUserRouter)
app.include_router(StockAdminRouter)


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    return failed_response(
        message=_http_message(exc.detail),
        error=exc.detail,
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return failed_response(
        message="Validation error",
        error=exc.errors(),
        status_code=422,
    )