from .Schemas import RegisterUser, UserLogin, Token
from .Models import User
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .Repository import IUserRepository, get_user_repository
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt


# ---------------- Security Service ----------------
class SecurityService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = "mG/xJYdH/b3bR9K2FJqaVUTAvrie2dQxdytkDQPUfGo="
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_minutes = 60 * 24 * 30 

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.refresh_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_security_service() -> SecurityService:
    return SecurityService()


# ---------------- Auth Service ----------------

class AuthService:
    def __init__(self, user_repository: IUserRepository, security_service: SecurityService):
        self.user_repository = user_repository
        self.security_service = security_service

    def get_user_by_email(self, email: str) -> User | None:
        return self.user_repository.get_user_by_email(email)

    def register_user(self, user: RegisterUser) -> User:
        if self.get_user_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if user.password != user.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        hashed_password = self.security_service.hash_password(user.password)
        new_user = User(name=user.name, phone=user.phone, email=user.email, password=hashed_password)
        
        return self.user_repository.create_user(new_user)

    def login_user(self, login_user: UserLogin) -> Token:
        user = self.get_user_by_email(login_user.email)
        if not user or not self.security_service.verify_password(login_user.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = self.security_service.create_access_token(data={"sub": user.email, "role": user.role.value})
        refresh_token = self.security_service.create_refresh_token(data={"sub": user.email, "role": user.role.value})
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer", role=user.role)

    def refresh_token(self, refresh_token: str) -> Token:
        try:
            payload = self.security_service.decode_token(refresh_token)
            email = payload.get("sub")
            role = payload.get("role")
            if email is None or role is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            user = self.get_user_by_email(email)
            if not user or user.role.value != role:
                raise HTTPException(status_code=401, detail="Invalid token")
            access_token = self.security_service.create_access_token(data={"sub": user.email, "role": user.role.value})
            return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer", role=user.role)
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

def get_auth_service(
    user_repository: IUserRepository = Depends(get_user_repository),
    security_service: SecurityService = Depends(get_security_service),
) -> "AuthService":
    return AuthService(user_repository, security_service)

