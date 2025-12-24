import re

from pydantic import BaseModel, Field, field_validator, ConfigDict


class CreateUserRequest(BaseModel):
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str = Field(min_length=8, max_length=32)
    admin: bool = False
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


class UserResponse(BaseModel):
    username: str
    first_name: str | None
    last_name: str | None
    email: str | None
    phone_number: str | None
    admin: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str | None = None
    priority: int = Field(ge=1, le=5)
    complete: bool


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: int
    complete: bool
    owner_id: int


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=8, max_length=32)
    new_password: str = Field(min_length=8, max_length=32)
