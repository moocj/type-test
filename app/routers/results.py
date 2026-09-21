"""
POST /api/results - posts a new finished type test
GET /api/results - gets the latest results
"""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlmodel import Session, select

from app.db import get_session
from app.models import Result
from app.services.stats import compute

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/api", tags=["results"])


class ResultIn(BaseModel):
    """
    Results the client can send, to hopefully prevent fake stat injections.
    """

    model_config = ConfigDict(extra="forbid")  # prevents injection

    target: str
    typed: str
    duration: float = Field(gt=0)
    per_second: list[float] = []
    mode: Literal["time", "words"]
    mode_value: int = Field(gt=0)
    list: str = "english_1k"


@router.post("/results", status_code=201)
def create_result(payload: ResultIn, session: SessionDep) -> Result:
    stats = compute(payload.target, payload.typed, payload.duration, payload.per_second)
    row = Result(
        wpm=stats["wpm"],
        raw=stats["raw"],
        acc=stats["accuracy"],
        consistency=stats["consistency"],
        chars=stats["chars"],
        correct=stats["correct"],
        errors=stats["errors"],
        mode=payload.mode,
        mode_value=payload.mode_value,
        list=payload.list,
        duration=payload.duration,
        target=payload.target,
        typed=payload.typed,
    )
    session.add(row)
    session.commit()
    session.refresh(row)

    return row


@router.get("/results")
def list_results(
    session: SessionDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[Result]:
    statement = (
        select(Result).order_by(Result.created_at.desc(), Result.id.desc()).limit(limit)
    )
    return list(session.exec(statement).all())
