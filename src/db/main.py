from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import Config
from sqlmodel import SQLModel
from src.db.models import Book


engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True,
    )
)

async def initdb():
    '''create a connection to our db'''

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    """Dependency to provide the session object"""

    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
