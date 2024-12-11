from datetime import datetime
import uuid

from sqlmodel import (SQLModel, Field, Column,)
import sqlalchemy.dialects.postgresql as pg

class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,  # Automatically generate a UUID
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    )
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )

    def __repr__(self) -> str:
        return f"<Book {self.title}>"

class User(SQLModel, table=True):
    __tablename__ = "user_accounts"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
            info={"description": "Unique identifier for the user account"},
        )
    )

    username: str
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = False
    email: str
    password_hash: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))

    def __repr__(self) -> str:
        return f"<User {self.username}>"