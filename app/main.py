from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db import create_db_and_tables
from app.routers import results, words


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="type-test", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Checks API is alive."""
    return {"status": "ok"}


app.include_router(words.router)
app.include_router(results.router)

app.mount("/", StaticFiles(directory="static"), name="static")
