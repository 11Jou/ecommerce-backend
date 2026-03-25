from fastapi import APIRouter, Depends, Body
from .Schemas import UserProfileResponse, UpdateUserProfile
from Modules.Auth.CheckAuth import get_current_user
from Modules.Auth.Models import User
from .Services import UserProfileService, get_user_profile_service

router = APIRouter(prefix="/user-profile", tags=["user-profile"])

@router.get("/", response_model=UserProfileResponse)
def get_user_profile_route(
    current_user: User = Depends(get_current_user),
    user_profile_service: UserProfileService = Depends(get_user_profile_service),
) -> UserProfileResponse:
    return user_profile_service.get_user_profile(current_user)


@router.put("/update", response_model=UserProfileResponse)
def update_user_profile_route(
    user_profile: UpdateUserProfile,
    current_user: User = Depends(get_current_user),
    user_profile_service: UserProfileService = Depends(get_user_profile_service),
) -> UserProfileResponse:
    return user_profile_service.update_current_user_profile(current_user, user_profile)