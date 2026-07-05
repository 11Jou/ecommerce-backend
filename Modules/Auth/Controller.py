from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Utils.Response import success_response

from .CheckAuth import get_current_user
from .Models import User
from .Schemas import *
from .Services import (
    AuthService,
    IActivationMailService,
    get_activation_mail_service,
    get_auth_service,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register_user_route(
    user: RegisterUser,
    auth_service: AuthService = Depends(get_auth_service),
    activation_mail_service: IActivationMailService = Depends(get_activation_mail_service),
) -> JSONResponse:
    new_user = await auth_service.register_user(user)
    await activation_mail_service.send_activation_mail(new_user)
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


@router.post("/activate")
async def activate_user_route(
    token: str,
    auth_service: AuthService = Depends(get_auth_service),
) -> JSONResponse:
    await auth_service.activate_user(token)
    return success_response(
        message="User activated successfully",
    )


@router.put("/resend-activation-mail")
async def resend_activation_mail_route(
    user: User = Depends(get_current_user),
    activation_mail_service: IActivationMailService = Depends(get_activation_mail_service),
) -> JSONResponse:
    await activation_mail_service.send_activation_mail(user)
    return success_response(
        message="Activation mail resent successfully",
    )


@router.post("/login")
async def login_user_route(
    login_user: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> JSONResponse:
    token = await auth_service.login_user(login_user)
    return success_response(
        data=token.model_dump(mode="json"),
        message="Login successful",
    )


@router.post("/refresh-token")
async def refresh_token_route(
    data: RefreshToken,
    auth_service: AuthService = Depends(get_auth_service),
) -> JSONResponse:
    token = await auth_service.refresh_token(data.refresh_token)
    return success_response(
        data=token.model_dump(mode="json"),
        message="Token refreshed",
    )


@router.put("/change-password")
async def change_password_route(
    data: ChangePassword,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> JSONResponse:
    await auth_service.change_password(current_user, data)
    return success_response(
        message="Password changed successfully",
    )
