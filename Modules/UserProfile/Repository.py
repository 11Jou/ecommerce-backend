from abc import ABC, abstractmethod
from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Database import get_db
from Modules.Auth.Models import User
from .Schemas import UpdateUserProfile


class IUserProfileRepository(ABC):
    @abstractmethod
    async def get_user_profile(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def update_user_profile(self, current_user: User, user_profile: UpdateUserProfile) -> User:
        pass


class UserProfileRepository(IUserProfileRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_profile(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def update_user_profile(self, current_user: User, user_profile: UpdateUserProfile) -> User:
        user = current_user
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        data = user_profile.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in data.items():
            setattr(user, key, value)

        user.updated_at = datetime.now()

        await self.db.commit()
        await self.db.refresh(user)
        return user


def get_user_profile_repository(db: AsyncSession = Depends(get_db)) -> IUserProfileRepository:
    return UserProfileRepository(db)
