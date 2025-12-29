"""Unit tests for admin routers API endpoints."""

from typing import Generator

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..models.todos import Todos
from .conftest import TestingSessionLocal


def test_admin_read_all_authenticated(
    client: TestClient, test_todo: Generator
) -> None:
    """Validate that an authenticated admin user can read all todos.

    Args:
        test_todo (Generator): The pre-seeded todo data instance.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 200 or the
            response body does not match the expected value.
    """
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "title": "Learn to code!",
            "description": "Need to learn everyday!",
            "priority": 5,
            "complete": False,
            "owner_id": 1,
        }
    ]


def test_admin_delete_todo(
    client: TestClient,
    test_todo: Generator,
) -> None:
    """Verify deletion of todo as an admin user.

    Args:
        test_todo (Generator): The pre-seeded todo data instance.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 204 or model
            is not deleted from database.
    """
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db: Session = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found(client: TestClient) -> None:
    """Test deleting a non-existent todo as an admin user.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 404 or the
            response body does not match the expected value.
    """
    response = client.delete("/admin/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not Found"}
