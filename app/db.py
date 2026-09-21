"""
Engine that stores session stats for the user.
"""

from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.models import Result  # noqa: F401

SQLITE_FILE = "type-test.db"

engine = create_engine(
    f"sqlite:///{SQLITE_FILE}",
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
    """
    Building tables directly from the models for now.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
