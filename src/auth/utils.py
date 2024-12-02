import uuid
from typing import Optional
from datetime import (datetime, timedelta)

import jwt
from passlib.context import CryptContext
from src.config import Config

passwd_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password:str) -> str:
    hash = passwd_context.hash(password)
    return hash

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password,hash)

def create_access_token(
        user_data:dict, expiry: timedelta = None, refresh: bool = False
) -> str:
    payload = {
        'user': user_data,
        'exp': datetime.now() + (expiry if expiry is not None else timedelta(minutes=60)),
        'jti': str(uuid.uuid4()),
        'refresh': refresh,
    }

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> Optional[dict]:
    try:
        # Decode the token using the secret key and algorithm
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,  # Replace with your secret key
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data

    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None