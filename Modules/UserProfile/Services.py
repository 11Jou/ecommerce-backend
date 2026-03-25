from fastapi import Depends
from .Repository import IUserProfileRepository, get_user_profile_repository
from .Schemas import UserProfileResponse, UpdateUserProfile
from Modules.Auth.Models import User


class UserProfileService:
    def __init__(self, user_profile_repository: IUserProfileRepository):
        self.user_profile_repository = user_profile_repository

    def get_user_profile(self, current_user: User) -> UserProfileResponse:
        return UserProfileResponse(
            id=current_user.id,
            name=current_user.name,
            phone=current_user.phone,
            email=current_user.email,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at,
        )

    def update_current_user_profile(self, current_user: User, user_profile: UpdateUserProfile) -> UserProfileResponse:
        updated_user_profile = self.user_profile_repository.update_user_profile(current_user, user_profile)
        return UserProfileResponse(
            id=updated_user_profile.id,
            name=updated_user_profile.name,
            phone=updated_user_profile.phone,
            email=updated_user_profile.email,
            created_at=updated_user_profile.created_at,
            updated_at=updated_user_profile.updated_at,
        )


def get_user_profile_service(user_profile_repository: IUserProfileRepository = Depends(get_user_profile_repository)) -> UserProfileService:
    return UserProfileService(user_profile_repository)