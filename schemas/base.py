from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    """A base schema with configuration for from_attributes."""

    model_config = ConfigDict(from_attributes=True)
