from fastapi import (APIRouter, HTTPException, status,)
from typing import List

from src.books.database import books
from src.books.schemas import (Book, UpdateBookRequest,)


router = APIRouter()

@router.get("/books", response_model=List[Book])
def get_all_books():
    return books

@router.post("/book", status_code=status.HTTP_201_CREATED)
def add_book(payload:Book) -> dict:
    new_book = payload.model_dump()
    books.append(new_book)

    return new_book

@router.get("/book/{book_id}", response_model=Book)
def get_book_by_id(book_id:int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book Not Found"
    )

@router.patch("/book/{book_id}")
def update_book(book_id:int,update_data:UpdateBookRequest) -> dict:
    for book in books:
        if book["id"] == book_id:
            if update_data.title is not None:
                book["title"] =  update_data.title
            if update_data.author is not None:
                book["author"] = update_data.author
            if update_data.publisher is not None:
                book["publisher"] = update_data.publisher
            if update_data.language is not None:
                book["language"] = update_data.language

            return book
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book Not Found"
    )



@router.delete("/book/{book_id}")
def delete_book(book_id:int):
    for book in books:
        if book["id"] == book_id:
            return books.remove(book)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book Not Found"
    )
    