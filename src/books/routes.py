from typing import List

from fastapi import (APIRouter, HTTPException, status, Depends,)
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.database import books
from src.books.schemas import (Book, UpdateBookRequest, BookCreateModel, BookResponse,)
from src.books.service import BookService
from src.db.main import get_session
from src.auth.dependencies import (AccessTokenBearer, RoleChecker,)


router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin","user"]))

@router.get("/", response_model=List[BookResponse], dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    books = await book_service.get_all_books(session=session)
    return [
        {
            "uid": book.uid,
            "title": book.title,
            "author":book.author,
            "publisher": book.publisher,
            "published_date": book.published_date.isoformat(),
            "page_count": book.page_count,
            "language": book.language,
            "created_at": book.created_at.isoformat(),
            "updated_at": book.updated_at.isoformat(),
        }
        for book in books
    ]

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def add_book(payload:BookCreateModel, session: AsyncSession = Depends(get_session), token_details=Depends(access_token_bearer)) -> dict:
    user_id =  token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(payload,user_id,session)

    return new_book.model_dump()

@router.get("/{book_uid}", response_model=BookResponse, dependencies=[role_checker])
async def get_book_by_id(
    book_uid:str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    book = await book_service.get_book(book_uid,session)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not Found"
        )
    
    return book

@router.patch("/{book_uid}", dependencies=[role_checker])
async def update_book(book_uid:str, update_data:UpdateBookRequest, session: AsyncSession = Depends(get_session),token_details=Depends(access_token_bearer),):
    updated_book = await book_service.update_book(book_uid, update_data, session)

    if not update_book: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not Found"
        )
    
    return updated_book



@router.delete("/{book_uid}", dependencies=[role_checker])
async def delete_book(book_uid:str,session: AsyncSession = Depends(get_session),token_details=Depends(access_token_bearer),):
    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not Found"
        )
    
    return {}
    