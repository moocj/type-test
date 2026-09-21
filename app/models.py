from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Result(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    wpm: float
    raw: float
    acc: float
    consistency: float
    chars: int  # keypresses
    correct: int
    errors: int

    # setup
    mode: str  # could play either with a time limit or a word limit
    mode_value: int
    list: str
    duration: float
    target: str
    typed: str

    created_at: datetime = Field(default_factory=_utcnow)
