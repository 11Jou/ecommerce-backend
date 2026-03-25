from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from datetime import datetime
from Core.Database import get_db
from Modules.Auth.Models import User
from .Schemas import UpdateUserProfile


class IUserProfileRepository(ABC):
    @abstractmethod
    def get_user_profile(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def update_user_profile(self, current_user: User, user_profile: UpdateUserProfile) -> User:
        pass

class UserProfileRepository(IUserProfileRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_user_profile(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user_profile(self, current_user: User, user_profile: UpdateUserProfile) -> User:
        user = current_user
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        data = user_profile.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in data.items():
            setattr(user, key, value)

        user.updated_at = datetime.now()

        self.db.commit()
        self.db.refresh(user)
        return user

def get_user_profile_repository(db: Session = Depends(get_db)) -> IUserProfileRepository:
    return UserProfileRepository(db)