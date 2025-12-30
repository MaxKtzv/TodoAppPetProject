"""Admin-related backend APIs for managing todo operations."""

from fastapi import APIRouter, Path, status

from dependencies.current_user import user_dependency
from dependencies.database.db import admin_service_dependency
from schemas.todos import TodoResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get(
    "/todo", status_code=status.HTTP_200_OK, response_model=list[TodoResponse]
)
def read_todos(user: user_dependency, service: admin_service_dependency):
    """HTTP backend endpoint for retrieving all todos.

    Accessible only to authenticated users with admin privileges.

    Args:
        user (dict): The context of the authenticated admin user
            provided by the dependency.
        service (AdminServices): A business logic layer dependency
            used to retrieve all todos.

    Returns:
        list[TodoResponse]: A list of all todo stored in the database.

    Raises:
        HTTPException: If admin authentication fails.
    """
    return service.get_all_todos(user)


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    user: user_dependency,
    service: admin_service_dependency,
    todo_id: int = Path(ge=1),
) -> None:
    """HTTP backend endpoint for deleting a todo by ID.

    Accessible only to authenticated users with admin privileges.

    Args:
        user (dict): The context of the authenticated admin user
            provided by the dependency.
        service (AdminServices): A business logic layer dependency
            used to delete a todo.
        todo_id (int): The ID of the todo to be deleted.

    Returns:
        None

    Raises:
        HTTPException: If admin authentication fails.
    """
    service.delete(user, todo_id)
