"""Unit tests for auth routers API endpoints."""

from datetime import timedelta

import pytest
from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from ..dependencies.current_user import get_current_user
from ..models.users import User
from ..security.constants import ALGORITHM, SECRET_KEY
from ..security.token import create_access_token
from ..services.auth.auth_services import AuthServices
from .conftest import TestingSessionLocal


def test_authenticate_user(test_user: User) -> None:
    """Test the authentication process for a user.

    Args:
        test_user (Generator): The pre-seeded user data instance.

    Returns:
        None.

    Raises:
        AssertionError: If the authentication process does not behave as
            expected.
    """
    db: Session = TestingSessionLocal()
    auth_services = AuthServices(db)
    authenticated_user = auth_services.authenticate_user(
        test_user.username, "test_password"
    )
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user: bool = auth_services.authenticate_user(
        "Wrong_user_name", "test_password"
    )
    assert non_existent_user is False

    wrong_password = auth_services.authenticate_user(
        test_user.username, "wrong_password"
    )
    assert wrong_password is False


def test_create_access_token() -> None:
    """Test validating the creation of an access token.

    Returns:
        None.

    Raises:
        AssertionError: If the decoded token does not contain the
            expected claims.
    """
    username = "test_user"
    user_id = 1
    whether_admin = False
    expires_delta = timedelta(days=1)
    token: str = create_access_token(username, user_id, whether_admin, expires_delta)
    decoded_token: dict = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"verify_signature": False},
    )
    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["admin"] == whether_admin


@pytest.mark.asyncio
async def test_get_current_user_valid_token() -> None:
    """Test the get_current_user async function with a valid token.

    Returns:
        None.

    Raises:
        AssertionError: If the function does not return the expected
            user details.
    """
    encode: dict = {"sub": "test_user", "id": 1, "admin": True}
    token: str = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user: dict = await get_current_user(token=token)
    assert user == {"username": "test_user", "id": 1, "admin": True}


@pytest.mark.asyncio
async def test_get_current_user_missing_playload() -> None:
    """Test behavior when provided with an invalid token payload.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 401 or the
            response body does not match the expected value.
    """
    encode: dict = {"admin": False}
    token: str = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Could not validate credentials"
