from abc import ABC, abstractmethod
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from Modules.Auth.Models import ActivationToken
from Core.Database.AsyncDatabase import get_db


class ITokenRepository(ABC):
    @abstractmethod
    async def create_token(self, token: ActivationToken) -> ActivationToken:
        pass

    @abstractmethod
    async def get_token_by_token(self, token: str) -> ActivationToken | None:
        pass

    @abstractmethod
    async def get_token_by_user_id(self, user_id: int) -> ActivationToken | None:
        pass

    @abstractmethod
    async def update_token(self, token: ActivationToken) -> ActivationToken:
        pass

    @abstractmethod
    async def delete_token(self, token: ActivationToken) -> None:
        pass

class TokenRepository(ITokenRepository):

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create_token(self, token: ActivationToken) -> ActivationToken:
        self.db.add(token)
        await self.db.commit()
        return token

    async def get_token_by_token(self, token: str) -> ActivationToken | None:
        result = await self.db.execute(
            select(ActivationToken)
            .options(joinedload(ActivationToken.user))
            .where(ActivationToken.token == token)
        )
        return result.scalars().first()

    async def get_token_by_user_id(self, user_id: int) -> ActivationToken | None:
        result = await self.db.execute(
            select(ActivationToken).where(ActivationToken.user_id == user_id)
        )
        return result.scalars().first()

    async def update_token(self, token: ActivationToken) -> ActivationToken:
        await self.db.commit()
        return token

    async def delete_token(self, token: ActivationToken) -> None:
        await self.db.delete(token)
        await self.db.commit()

def get_token_repository(db: AsyncSession = Depends(get_db)) -> ITokenRepository:
    return TokenRepository(db)