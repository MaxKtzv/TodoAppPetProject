"""Define data schemas for todo application requests and responses."""

from pydantic import Field

from schemas.base import Base


class TodoRequest(Base):
    """A data schema for todo creation and update requests."""

    title: str = Field(min_length=3)
    description: str | None = None
    priority: int = Field(ge=1, le=5)
    complete: bool


class TodoResponse(Base):
    """A data schema for todo responses."""

    id: int
    title: str
    description: str
    priority: int
    complete: bool
    owner_id: int
