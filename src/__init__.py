from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.books.routes import router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
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

app.include_router(auth_router,prefix=f"/api/{version}/auth",tags=["authentication"])
app.include_router(router, prefix=f"/api/{version}/books",tags=['books'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])