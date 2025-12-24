from fastapi import status

from .utils import (
    TestingSessionLocal,
    client,
    override_get_current_user,
    override_get_db,
    test_user,
)


def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "test_admin"
    assert response.json()["email"] == "test@email.com"
    assert response.json()["first_name"] == "Test"
    assert response.json()["last_name"] == "User"
    assert response.json()["admin"]
    assert response.json()["phone_number"] == "+1 (123) 456-7890"


def test_change_password_success(test_user):
    response = client.put(
        "/user/password",
        json={
            "old_password": "testpassword",
            "new_password": "changed_to_newpassword",
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_old_password(test_user):
    response = client.put(
        "/user/password",
        json={
            "old_password": "wrong_password",
            "new_password": "changed_to_newpassword",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_change_phone_number_success(test_user):
    response = client.put("/user/phone_number?phone_number=%2B1%20(800)%20895-3601")
    assert response.status_code == status.HTTP_204_NO_CONTENT
