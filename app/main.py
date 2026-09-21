from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="type-test", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Checks API is alive."""
    return {"status": "ok"}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
