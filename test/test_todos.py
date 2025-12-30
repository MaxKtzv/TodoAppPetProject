"""Unit tests for todos routers API endpoints."""

from typing import Generator

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.todos import Todos
from test.conftest import TestingSessionLocal


def test_read_all_authenticated(
    client: TestClient, test_todo: Generator
) -> None:
    """Test retrieval of all todos for an authenticated user.

    Args:
        test_todo (Generator): The pre-seeded todo data instance.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 200 or the
            response body does not match the expected value.
    """
    response = client.get("/todos")
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


def test_read_one_authenticated(client: TestClient, test_todo: Generator):
    """Test retrieval of a todo by ID for an authenticated user.

    Args:
        test_todo (Generator): The pre-seeded todo data instance.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 200 or the
            response body does not match the expected value.
    """
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Learn to code!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False,
        "owner_id": 1,
    }


def test_read_one_authenticated_not_found(client: TestClient) -> None:
    """Test retrieval of a non-existent todo.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 404 or the
            returned error message is incorrect.
    """
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not Found"}


def test_create_todo(
    client: TestClient,
    test_todo: Generator,
) -> None:
    """Test creation of a new todo for an authenticated user.

    Args:
        test_todo (Generator): The pre-seeded todo data instance.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 201 or the
            response body does not match the expected value.
    """
    request_data = {
        "title": "New Todo!",
        "description": "New todo description",
        "priority": 5,
        "complete": False,
    }

    response = client.post("/todos/todo/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    db: Session = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(
    client: TestClient,
    test_todo: Generator,
) -> None:
    """Test update of a todo for the authenticated user.

    Args:
        test_todo (Generator): The pre-seeded todo data instance.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 204 or the
            response body does not match the expected value.
    """
    request_data = {
        "title": "Change the title of the todo already created!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todos/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db: Session = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "Change the title of the todo already created!"


def test_update_todo_not_found(client: TestClient, test_todo: Generator):
    """Test update of a non-existent todo.

    Args:
        test_todo (Generator): The pre-seeded todo data instance.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 404 or the
            response body does not match the expected value.
    """
    request_data = {
        "title": "Change the title of the todo already created!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todos/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not Found"}


def test_delete_todo(
    client: TestClient,
    test_todo: Generator,
):
    """Test deletion of a todo for the authenticated user.

    Args:
        test_todo (Generator): The pre-seeded todo data instance.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 204 or model
            is not deleted from database.
    """
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db: Session = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found(
    client: TestClient, test_todo: Generator
) -> None:
    """Test deletion of a non-existent todo.

    Args:
        test_todo (Generator): The pre-seeded todo data instance.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 404 or the
            response body does not match the expected value.
    """
    response = client.delete("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not Found"}
