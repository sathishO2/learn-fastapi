from fastapi import FastAPI

from src.books.router import router

version = "v1"

app = FastAPI(
    title="Bookly",
    description="to learn fast-api",
    version=version,
)

app.include_router(router, prefix=f"/api/{version}/books",tags=['books'])