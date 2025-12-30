"""Unit tests for validating functionalities in users routers API endpoints."""

from typing import Generator

from fastapi import status
from fastapi.testclient import TestClient


def test_return_user(client: TestClient, test_user: Generator) -> None:
    """Validate retrieval of user information.

    Args:
        test_user (Generator): The pre-seeded user data instance.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 200 or the
            response body does not match the expected value.
    """
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "test_admin"
    assert response.json()["email"] == "test@email.com"
    assert response.json()["first_name"] == "Test"
    assert response.json()["last_name"] == "User"
    assert response.json()["admin"]
    assert response.json()["phone_number"] == "+1 (123) 456-7890"


def test_change_profile_success(
    client: TestClient, test_user: Generator
) -> None:
    """Test successful change of a user's profile information.

    Args:
        test_user (Generator): The pre-seeded user data instance.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 204 or the
            response body does not match the expected value.
    """
    response = client.put(
        "/user/update",
        json={
            "old_password": "test_password",
            "new_password": "changed_to_newpassword",
            "username": "new_username",
            "email": "new_email@example.com",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "phone_number": "+1 (800) 895-3601",
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_profile_invalid_old_password(
    client: TestClient, test_user: Generator
) -> None:
    """Test profile update when an invalid password is provided.

    Args:
        test_user (Generator): The pre-seeded user data instance.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 401 or the
            response body does not match the expected value.
    """
    response = client.put(
        "/user/update",
        json={
            "old_password": "wrong_password",
            "new_password": "changed_to_newpassword",
            "username": "new_username",
            "email": "new_email@example.com",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "phone_number": "+1 (800) 895-3601",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
