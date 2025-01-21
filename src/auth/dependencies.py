from typing import List

from fastapi.security import (HTTPBearer, HTTPAuthorizationCredentials,)
from fastapi import (Request, status, Depends,)
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from .utils import decode_token
from src.db.main import get_session
from .service import (UserService, User,)
# from src.db.redis import token_in_blocklist
from src.errors import (
    InvalidToken,
    RefreshTokenRequired,
    AccessTokenRequired,
    InsufficientPermission,
)

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials 

        token_data = decode_token(token)

        # if await token_in_blocklist(token_data['jti']):
        #     raise InvalidToken()

        if not self.token_valid(token):
            raise InvalidToken()
        
        return token_data
    
    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)

        return token_data is not None
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise AccessTokenRequired()

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        raise RefreshTokenRequired()

async def get_current_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session),
):
    user_email = token_details['user']['email']
    user = await user_service.get_user_by_email(user_email, session)
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user:User = Depends(get_current_user)):
        if current_user.role in self.allowed_roles:
            return True
        
        raise InsufficientPermission()