from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends , HTTPException, status
from .Services import AuthService, get_auth_service
from .Models import User
from typing import List

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service)
):
    token = credentials.credentials
    payload = auth_service.security_service.decode_token(token)
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = auth_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_role(allowed_roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.value not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user
    return role_checker