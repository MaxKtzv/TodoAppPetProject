from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str = Field(min_length=8, max_length=32)
    admin: bool = False
    phone_number: int | None = Field(ge=1000000000, le=9999999999, default=None)


class UserResponse(BaseModel):
    username: str
    first_name: str | None
    last_name: str | None
    email: str | None
    phone_number: int | None
    admin: bool

    class ConfigDic:
        from_attributes = True


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
