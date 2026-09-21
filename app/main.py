from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import words

app = FastAPI(title="type-test", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Checks API is alive."""
    return {"status": "ok"}


app.include_router(words.router)

app.mount("/", StaticFiles(directory="static"), name="static")
