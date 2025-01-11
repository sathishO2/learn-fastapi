from datetime import (datetime,timedelta,)

from fastapi import (APIRouter, Depends, status,)
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from src.config import Config
from src.db.main import get_session
from .schemas import (UserCreateModel,UserLoginModel, UserBooksModel)
from .utils import create_access_token, verify_password
from .service import UserService
from .dependencies import (RefreshTokenBearer, AccessTokenBearer, RoleChecker, get_current_user,)
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service =  UserService()
role_checker = RoleChecker(["admin","user"])

REFRESH_TOKEN_EXPIRY = 6000

@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(
    user=Depends(get_current_user),
    _: bool = Depends(role_checker)
):
    user_dict = {
        "uid": user.uid,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_verified": user.is_verified,
        "password_hash": user.password_hash,
        "created_at": user.created_at.isoformat(),
        "books": [
            {
                "uid": book.uid,
                "title": book.title,
                "author": book.author,
                "publisher": book.publisher,
                "published_date": book.published_date.isoformat(),
                "page_count": book.page_count,
                "language": book.language,
            }
            for book in user.books
        ],
    }
    return user_dict

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email,session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists"
        )
    
    new_user = await user_service.create_user(user_data,session)

    return new_user

@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email,session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid Email"
        )
    
    password_valid = verify_password(password, user.password_hash)

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid Password"
        )
    
    access_token = create_access_token(
        user_data={"email":user.email, "user_uid": str(user.uid)}
    )

    refresh_token = create_access_token(
        user_data={
            "email":user.email, "user_uid": str(user.uid)
        },
        refresh=True,
        expiry=timedelta(minutes=REFRESH_TOKEN_EXPIRY)
    )

    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {"email": user.email, "uid": str(user.uid)},
        }
    )

@auth_router.get("/refresh_token")
async def get_new_access_token(token_data: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_data['exp']

    if datetime.fromtimestamp(expiry_timestamp) < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    new_access_token =  create_access_token(user_data=token_data['user'])

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "access_token": new_access_token
        }
    )

@auth_router.get("/logout")
async def revoke_token(token_details: dict=Depends(AccessTokenBearer())):

    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message": "logged out Successfully"
        },
        status_code=status.HTTP_200_OK
    )