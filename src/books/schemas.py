
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import uuid

class Book(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookResponse(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime
class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    
class UpdateBookRequest(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None
