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


@router.get("/profile", response_model=ProfileResponse)
def get_profile_route(
    current_user: User = Depends(get_current_user),
) -> ProfileResponse:
    return ProfileResponse(
        id=current_user.id,
        name=current_user.name,
        phone=current_user.phone,
        email=current_user.email,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.put("/profile", response_model=ProfileResponse)
def update_profile_route(
    update_user: UpdateUser,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> ProfileResponse:
    return auth_service.update_user(update_user, current_user)



@router.delete("/profile/{user_id}")
def delete_profile_route(
    user_id: int,
    current_user: User = Depends(require_role([Role.ADMIN])),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    auth_service.delete_user(user_id)
    return {"message": "User deleted successfully"}