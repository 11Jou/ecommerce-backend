from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Utils.Response import success_response

from .Schemas import *
from .Services import AuthService, get_auth_service
from .CheckAuth import get_current_user
from .Models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register_user_route(
    user: RegisterUser,
    auth_service: AuthService = Depends(get_auth_service),
) -> JSONResponse:
    new_user = auth_service.register_user(user)
    body = UserResponse(
        id=new_user.id,
        email=new_user.email,
        role=new_user.role,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at,
    )
    return success_response(
        data=body.model_dump(mode="json"),
        message="Registered successfully",
        status_code=201,
    )


@router.post("/login")
def login_user_route(
    login_user: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> JSONResponse:
    token = auth_service.login_user(login_user)
    return success_response(
        data=token.model_dump(mode="json"),
        message="Login successful",
    )


@router.post("/refresh-token")
def refresh_token_route(
    data: RefreshToken,
    auth_service: AuthService = Depends(get_auth_service),
) -> JSONResponse:
    token = auth_service.refresh_token(data.refresh_token)
    return success_response(
        data=token.model_dump(mode="json"),
        message="Token refreshed",
    )


@router.put("/change-password")
def change_password_route(
    data: ChangePassword,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> JSONResponse:
    auth_service.change_password(current_user, data)
    return success_response(
        message="Password changed successfully",
    )