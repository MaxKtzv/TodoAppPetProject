"""A module defining data schemas for user-related requests."""

import re

from pydantic import Field, field_validator

from schemas.base import Base


class BaseUserRequest(Base):
    """Represents a base schema for user-related requests.

    Provides empty strings conversion to None; phone number and email
    validation.
    """

    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None

    @field_validator(
        "email", "first_name", "last_name", "phone_number", mode="before"
    )
    @classmethod
    def empty_string_to_none(cls, v):
        if isinstance(v, str) and v.strip() == "":
            return None
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        if v is None:
            return v
        regex = r"^\+\d{1,3} \(\d{3}\) \d{3}-\d{4}$"
        if not re.match(regex, v):
            raise ValueError("Invalid phone number format")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v is None:
            return v
        regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(regex, v):
            raise ValueError("Invalid email format")
        return v


class CreateUserRequest(BaseUserRequest):
    """A data schema for user creation requests."""

    password: str = Field(min_length=8, max_length=32)
    admin: bool = False


class UpdateUserRequest(BaseUserRequest):
    """A data schema for user update requests."""

    old_password: str = Field(min_length=8, max_length=32)
    new_password: str = Field(min_length=8, max_length=32)


class UserResponse(Base):
    """A data schema for user responses."""

    username: str
    first_name: str | None
    last_name: str | None
    email: str | None
    phone_number: str | None
    admin: bool
