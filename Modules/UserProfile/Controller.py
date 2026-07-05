from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Modules.Auth.CheckAuth import get_current_verified_user
from Modules.Auth.Models import User
from .Schemas import UpdateUserProfile, UserProfileResponse
from .Services import UserProfileService, get_user_profile_service
from Utils.Response import success_response

router = APIRouter(prefix="/user-profile", tags=["user-profile"])


@router.get("/")
async def get_user_profile_route(
    current_user: User = Depends(get_current_verified_user),
    user_profile_service: UserProfileService = Depends(get_user_profile_service),
) -> JSONResponse:
    profile: UserProfileResponse = user_profile_service.get_user_profile(current_user)
    return success_response(
        data=profile.model_dump(mode="json"),
        message="Profile retrieved",
    )


@router.put("/update")
async def update_user_profile_route(
    user_profile: UpdateUserProfile,
    current_user: User = Depends(get_current_verified_user),
    user_profile_service: UserProfileService = Depends(get_user_profile_service),
) -> JSONResponse:
    profile: UserProfileResponse = await user_profile_service.update_current_user_profile(
        current_user, user_profile
    )
    return success_response(
        data=profile.model_dump(mode="json"),
        message="Profile updated",
    )
