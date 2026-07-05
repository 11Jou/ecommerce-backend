from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from jose import JWTError

from Modules.Auth.Models import ActivationToken, User
from Modules.Auth.Repository import IUserRepository, get_user_repository
from Modules.Auth.Schemas import ChangePassword, RegisterUser, Token, UserLogin
from Modules.Auth.Services.SecurityService import SecurityService, get_security_service
from Modules.Auth.Repository import ITokenRepository, get_token_repository


class AuthService:
    def __init__(self, user_repository: IUserRepository, security_service: SecurityService, token_repository: ITokenRepository):
        self.user_repository = user_repository
        self.security_service = security_service
        self.token_repository = token_repository

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repository.get_user_by_email(email)

    async def register_user(self, user: RegisterUser) -> User:
        if await self.get_user_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if user.password != user.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        hashed_password = self.security_service.hash_password(user.password)
        new_user = User(
            name=user.name,
            phone=user.phone,
            email=user.email,
            password=hashed_password,
        )

        return await self.user_repository.create_user(new_user)

    async def login_user(self, login_user: UserLogin) -> Token:
        user = await self.get_user_by_email(login_user.email)
        if not user or not self.security_service.verify_password(login_user.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = self.security_service.create_access_token(
            data={"sub": user.email, "role": user.role.value}
        )
        refresh_token = self.security_service.create_refresh_token(
            data={"sub": user.email, "role": user.role.value}
        )
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            role=user.role,
            is_verified=user.is_verified,
        )

    async def refresh_token(self, refresh_token: str) -> Token:
        try:
            payload = self.security_service.decode_token(refresh_token)
            email = payload.get("sub")
            role = payload.get("role")
            if email is None or role is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            user = await self.get_user_by_email(email)
            if not user or user.role.value != role:
                raise HTTPException(status_code=401, detail="Invalid token")
            access_token = self.security_service.create_access_token(
                data={"sub": user.email, "role": user.role.value}
            )
            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                role=user.role,
                is_verified=user.is_verified,
            )
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def change_password(self, current_user: User, data: ChangePassword) -> User:
        if not self.security_service.verify_password(data.old_password, current_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        if data.new_password != data.confirm_new_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        current_user.password = self.security_service.hash_password(data.new_password)
        return await self.user_repository.update_user(current_user)

    async def create_activation_token(self, user: User) -> ActivationToken:
        token = self.security_service.generate_secret_token()

        existing_token = await self.token_repository.get_token_by_user_id(user.id)
        if existing_token:
            existing_token.token = token
            existing_token.is_used = False
            existing_token.expires_at = datetime.now() + timedelta(minutes=15)
            existing_token.updated_at = datetime.now()
            return await self.token_repository.update_token(existing_token)

        activation_token = ActivationToken(
            token=token,
            user_id=user.id,
        )
        return await self.token_repository.create_token(activation_token)

    async def activate_user(self, token: str) -> User:
        activation_token = await self.token_repository.get_token_by_token(token)
        if not activation_token:
            raise HTTPException(status_code=404, detail="Activation token not found")
        if activation_token.is_used:
            raise HTTPException(status_code=400, detail="Activation token already used")
        if activation_token.expires_at < datetime.now():
            raise HTTPException(status_code=400, detail="Activation token expired")

        user = activation_token.user
        user.is_verified = True
        activation_token.is_used = True
        await self.token_repository.update_token(activation_token)
        return user


def get_auth_service(
    user_repository: IUserRepository = Depends(get_user_repository),
    security_service: SecurityService = Depends(get_security_service),
    token_repository: ITokenRepository = Depends(get_token_repository),
) -> AuthService:
    return AuthService(user_repository, security_service, token_repository)
