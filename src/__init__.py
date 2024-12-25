from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.books.router import router
from src.db.main import initdb

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting...")
    await initdb()
    yield
    print("Server is stoping.")

version = "v1"

app = FastAPI(
    title="Bookly",
    description="to learn fast-api",
    version=version,
    # lifespan=lifespan,
)

app.include_router(router, prefix=f"/api/{version}/books",tags=['books'])