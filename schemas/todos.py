from pydantic import Field, field_validator

from ..schemas.base import Base


class TodoRequest(Base):
    title: str = Field(min_length=3)
    description: str | None = None
    priority: int = Field(ge=1, le=5)
    complete: bool


class TodoResponse(Base):
    id: int
    title: str
    description: str
    priority: int
    complete: bool
    owner_id: int
