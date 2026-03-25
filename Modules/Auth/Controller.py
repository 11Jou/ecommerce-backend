from fastapi import APIRouter, Depends
from .Schemas import *
from .Services import AuthService, get_auth_service
from .CheckAuth import get_current_user, require_role
from .Models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register_user_route(
    user: RegisterUser,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    new_user = auth_service.register_user(user)
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        role=new_user.role,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at,
    )


@router.post("/login")
def login_user_route(
    login_user: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    return auth_service.login_user(login_user)


@router.post("/refresh-token")
def refresh_token_route(
    data: RefreshToken,
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    return auth_service.refresh_token(data.refresh_token)