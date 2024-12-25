from datetime import datetime

from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from src.books.schemas import (BookCreateModel, UpdateBookRequest,)
from sqlmodel import (select, desc, )


class BookService:
    '''
    This class provides methods to create, read, update, and delete books
    '''

    async def get_all_books(self, session: AsyncSession):
        """
        Get a list of all books

        Returns:
            list: list of books
        """

        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)

        return result.all()
    
    async def get_user_books(self, user_uid: str, session:AsyncSession):
        statement = (
            select(Book)
            .where(Book.user_uid == user_uid)
            .order_by(desc(Book.created_at))
        )

        result = await session.exec(statement)

        return result.all()
    
    async def create_book(self, book_data: BookCreateModel, user_uid: str, session: AsyncSession) -> Book:
        """
        Create a new Book

        Args:
            book_data (BookCreateModel): data to create a new book
        
        Returns:
            Book: the new book
        """

        book_data_dict  = book_data.model_dump()

        new_book = Book(
            **book_data_dict
        )

        new_book.user_uid = user_uid

        new_book.published_date = book_data_dict['published_date']# datetime.strptime(book_data_dict['published_date'],"%Y-%m-%d")

        session.add(new_book)

        await session.commit()

        return new_book
    
    async def get_book(self, book_uid:str, session: AsyncSession):
        """Get a Book by its UUID

        Args:
            book_uid (str): the UUID of the Book
        
        Returns:
            Book: the book object
        """

        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)

        book = result.first()

        return book if book is not None else None
    
    async def update_book(self, book_uid:str,update_date: UpdateBookRequest, session: AsyncSession):
        """Update a book info

        Args:
            book_uid (str):  the UUID of the book
            update_date (UpdateBookRequest): the date to update the book 
        
        Returns:
            Book: the updated book 
        """

        book_to_update = await self.get_book(book_uid,session)

        if book_to_update is not None:
            update_date_dict = update_date.model_dump()

            for k, v in update_date_dict.items():
                setattr(book_to_update,k,v)

            await session.commit()

            return book_to_update
        else:
            return None 
    
    async def delete_book(self, book_uid:str, session: AsyncSession):
        """Delete a book

        Args:
            book_uid (str): the UUID of the Book
        """

        book_to_delete = await self.get_book(book_uid,session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()

            return {}
        else:
            return None


