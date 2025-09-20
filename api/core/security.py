from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from services.users import get_user_by_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    async def __call__(self, token: str = Depends(oauth2_scheme)):
        user = await get_current_user(token)
        if not user or not any(role in self.allowed_roles for role in user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )