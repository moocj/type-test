"""
Gets a fresh set of words for the user to type.
"""

from fastapi import APIRouter, HTTPException, Query

from app.services.words import UnknownListError, generate

router = APIRouter(prefix="/api", tags=["words"])


@router.get("/words")
def get_words(
    count: int = Query(50, ge=1, le=500),
    list: str = Query("english_1k"),
    seed: int | None = Query(None),
) -> list[str]:
    try:
        return generate(count=count, list_name=list, seed=seed)
    except UnknownListError:
        raise HTTPException(status_code=404, detail=f"Unknown list: {list!r}") from None
