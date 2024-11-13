from typing import List

from fastapi import (APIRouter, HTTPException, status, Depends,)
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.database import books
from src.books.schemas import (Book, UpdateBookRequest, BookCreateModel, BookResponse,)
from src.books.service import BookService
from src.db.main import get_session


router = APIRouter()
book_service = BookService()

@router.get("/", response_model=List[Book])
async def get_all_books(
    session: AsyncSession = Depends(get_session)
):
    books = await book_service.get_all_books(session=session)
    return books

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_book(payload:BookCreateModel, session: AsyncSession = Depends(get_session)) -> dict:
    new_book = await book_service.create_book(payload,session)

    return new_book.model_dump()

@router.get("/{book_uid}", response_model=BookResponse)
async def get_book_by_id(
    book_uid:str,
    session: AsyncSession = Depends(get_session)
):
    book = await book_service.get_book(book_uid,session)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not Found"
        )
    
    return book

@router.patch("/{book_uid}")
async def update_book(book_uid:str, update_data:UpdateBookRequest, session: AsyncSession = Depends(get_session)):
    updated_book = await book_service.update_book(book_uid, update_data, session)

    if not update_book: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not Found"
        )
    
    return updated_book



@router.delete("/{book_uid}")
async def delete_book(book_uid:str,session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not Found"
        )
    
    return {}
    