from sqlalchemy.orm import Session
from fastapi import Depends
from Core.Database import get_db
from .Models import User
from abc import ABC, abstractmethod


def get_user_repository(db: Session = Depends(get_db)) -> "IUserRepository":
    return UserRepository(db)


class IUserRepository(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    def delete_user(self, user: User) -> User:
        pass



class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_user(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.db.delete(user)
        self.db.commit()
        return {"message": "User deleted successfully"}