from datetime import datetime, timedelta

import pytest
from fastapi import HTTPException, status
from jose import jwt

from ..dependencies.user import (
    ALGORITHM,
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from .utils import (
    TestingSessionLocal,
    test_user,
)


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "testpassword", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user("Wrong_user_name", "testpassword", db)
    assert non_existent_user is False

    wrong_password = authenticate_user(test_user.username, "wrong_password", db)
    assert wrong_password is False


def test_create_access_token():
    username = "test_user"
    user_id = 1
    whether_admin = False
    expires_delta = timedelta(days=1)
    token = create_access_token(username, user_id, whether_admin, expires_delta)
    decoded_token = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"verify_signature": False},
    )
    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["admin"] == whether_admin


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub": "test_user", "id": 1, "admin": True}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token=token)
    assert user == {"username": "test_user", "id": 1, "admin": True}


@pytest.mark.asyncio
async def test_get_current_user_missing_playload():
    encode = {"admin": False}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Could not validate credentials"
