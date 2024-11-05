from fastapi import FastAPI, HTTPException
from typing import (Optional, Dict,)

from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message":"hello world"
    }

@app.get("/greet/")
def greet(username: Optional[str] = "Your Name!"):
    return {
        "message":f"Hello, {username}"
    }

phone_list = [
    "samsung",
    "apple",
    "vivo",
    "oppo",
    "mi"
]

@app.get("/search")
def search_for_phone(brand:str):
    if brand in phone_list:
        return {
            "message": f"{brand} is available"
        }
    else:
        return {
            "message": f"{brand} is not available"
        }

user_db:Dict[str, str] = {}

class CreateUserRequest(BaseModel):
    username: str
    email: str

@app.post("/create_user")
def create_user(payload: CreateUserRequest):

    if payload.email in user_db:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    user_db[payload.email] = payload.username

    return {
        "message": "User Created Successfully",
        "user": payload
    }

