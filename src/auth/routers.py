from datetime import timedelta

from fastapi import (APIRouter, Depends, status,)
from .schemas import (UserCreateModel,UserLoginModel,)
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import create_access_token, verify_password
from fastapi.responses import JSONResponse
from src.config import Config

auth_router = APIRouter()
user_service =  UserService()

REFRESH_TOKEN_EXPIRY = 6000

@auth_router.post(
    "/signup", status_code=status.HTTP_201_CREATED
)
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