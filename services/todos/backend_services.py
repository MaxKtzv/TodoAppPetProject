"""Provides business logic handling for the todos API endpoints."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.todos import Todos
from schemas.todos import TodoRequest


class TodoService:
    """Provides functionality to perform CRUD operations on todo items.

    Attributes:
        db (Session): Database session for querying and manipulating data.
    """

    def __init__(self, db: Session):
        """Initialize the TodoService class."""
        self.db = db

    def get_all(self, user: dict):
        """Retrieve all todos for the authenticated user.

        Args:
            user (dict): Dictionary containing user information.

        Returns:
            list[Todos]: List of todos belonging to the specified user.

        Raises:
            HTTPException: If user authentication fails.
        """
        return (
            self.db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
        )

    def get_by_id(self, user: dict, todo_id: int):
        """Retrieve a todo by ID for the authenticated user.

        Args:
            user (dict): Dictionary containing user information.
            todo_id (int): The ID of the todo.

        Returns:
            Todos: The todo matching the given ID.

        Raises:
            HTTPException: If user authentication fails or the todo item
                is not found or does not belong to the user.
        """
        todo = (
            self.db.query(Todos)
            .filter(Todos.id == todo_id, Todos.owner_id == user.get("id"))
            .first()
        )
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return todo

    def create(self, user: dict, request: TodoRequest) -> None:
        """Create and add to database a new todo.

        Args:
            user (dict): Dictionary containing user information.
            request (TodoRequest): The todo creation request schema.

        Returns:
            None.

        Raises:
            HTTPException: If user authentication fails.
        """
        todo: Todos = Todos(**request.model_dump(), owner_id=user.get("id"))

        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)

    def update(self, user: dict, todo_id: int, request: TodoRequest) -> None:
        """Update the details of an existing todo.

        Args:
            user (dict): Dictionary containing user information.
            todo_id (int): The ID of the todo to be updated.
            request (TodoRequest): The todo creation request schema.

        Returns:
            None.

        Raises:
            HTTPException: If user authentication fails or the todo item
                is not found or does not belong to the user.
        """
        todo: Todos = self.get_by_id(user, todo_id)
        todo.title = request.title
        todo.description = request.description
        todo.priority = request.priority
        todo.complete = request.complete

        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)

    def delete(self, user, todo_id: int) -> None:
        """Delete a todo for the authenticated user.

        Args:
            user (dict): Dictionary containing user information.
            todo_id (int): The ID of the todo to be deleted.

        Returns:
            None.

        Raises:
            HTTPException: If user authentication fails or the todo item
                is not found or does not belong to the user.
        """
        todo: Todos = self.get_by_id(user, todo_id)

        self.db.delete(todo)
        self.db.commit()
