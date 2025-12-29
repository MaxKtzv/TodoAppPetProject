"""A collection of user-related APIs for managing todo operations."""

from fastapi import APIRouter, Path, Request, status

from ..dependencies.current_user import (
    user_dependency,
)
from ..dependencies.database.db import (
    todo_endpoint_dependency,
    todo_page_dependency,
)
from ..schemas.todos import TodoRequest, TodoResponse

router = APIRouter(prefix="/todos", tags=["todos"])


### Pages ###
@router.get("/todo-page")
async def get_todos_page(request: Request, service: todo_page_dependency):
    """HTTP frontend endpoint for retrieving a todo data page.

    Args:
        request (Request): The HTTP request object representing the
            client's request.
        service (TodoPageService): A business logic layer dependency
            used to retrieve a todo data page.

    Returns:
        TemplateResponse: An object rendering the "todo.html" page if
            the user is authenticated.

    Raises:
        RedirectResponse: A HTTP redirect response to the login page
            if authentication fails.
    """
    return await service.get_page(request)


@router.get("/add-todo-page")
async def add_todos_page(request: Request, service: todo_page_dependency):
    """HTTP frontend endpoint for retrieving an add todo page.

    Args:
        request (Request): The HTTP request object representing the
            client's request.
        service (TodoPageService): A business logic layer dependency
            used to retrieve an add todo page.

    Returns:
        TemplateResponse: An object rendering the "add-todo.html" page
            if the user is authenticated.

    Raises:
        RedirectResponse: A HTTP redirect response to the login page
            if authentication fails.
    """
    return await service.add_page(request)


@router.get("/edit-todo-page/{todo_id}", status_code=status.HTTP_200_OK)
async def edit_todos_page(
    request: Request,
    service: todo_page_dependency,
    todo_id: int = Path(ge=1),
):
    """HTTP frontend endpoint for retrieving an edit todo page.

    Args:
        request (Request): The HTTP request object representing the
            client's request.
        service (TodoPageService): A business logic layer dependency
            used to retrieve an edit todo page.
        todo_id (int): The ID of the todo to be edited.

    Returns:
        TemplateResponse: An object rendering the "edit-todo.html" page
            if the user is authenticated.

    Raises:
        RedirectResponse: A HTTP redirect response to the login page
            if authentication fails.
    """
    return await service.edit_page(request, todo_id)


### Endpoints ###
@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[TodoResponse]
)
def read_all(user: user_dependency, service: todo_endpoint_dependency):
    """HTTP backend endpoint for retrieving all todos.

    Accessible only to authenticated users.

    Args:
        user (dict): Dictionary containing user information.
        service (TodoService): A business logic layer dependency used
            to retrieve all todos for the specified user.

    Returns:
        list[TodoResponse]: List of todos belonging to the specified
            user.

    Raises:
        HTTPException: If user authentication fails.
    """
    return service.get_all(user)


@router.get(
    "/todo/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_model=TodoResponse,
)
def read_one(
    user: user_dependency,
    service: todo_endpoint_dependency,
    todo_id: int = Path(ge=1),
):
    """HTTP backend endpoint for retrieving a todo by ID.

    Accessible only to authenticated users.

    Args:
        user (dict): Dictionary containing user information.
        service (TodoService): A business logic layer dependency used
            to retrieve todo by ID.
        todo_id (int): The ID of the todo.

    Returns:
        TodoResponse: The todo matching the given ID.

    Raises:
        HTTPException: If user authentication fails or the todo item is
            not found or does not belong to the user.
    """
    return service.get_by_id(user, todo_id)


@router.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(
    user: user_dependency,
    request: TodoRequest,
    service: todo_endpoint_dependency,
) -> None:
    """HTTP backend endpoint for retrieving a todo creation.

    Accessible only to authenticated users.

    Args:
        user (dict): Dictionary containing user information.
        request (TodoRequest): The todo creation request schema.
        service (TodoService): A business logic layer dependency used
            to create a todo.

    Returns:
        None.

    Raises:
        HTTPException: If user authentication fails.
    """
    service.create(user, request)


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(
    user: user_dependency,
    request: TodoRequest,
    service: todo_endpoint_dependency,
    todo_id: int = Path(ge=1),
):
    """HTTP backend endpoint for retrieving a todo update.

    Accessible only to authenticated users.

    Args:
        user (dict): Dictionary containing user information.
        request (TodoRequest): The todo update request schema.
        service (TodoService): A business logic layer dependency used
            to update a todo.
        todo_id (int): The ID of the todo to be updated.

    Returns:
        None.

    Raises:
        HTTPException: If user authentication fails or the todo item is
            not found or does not belong to the user.
    """
    service.update(user, todo_id, request)


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    user: user_dependency,
    service: todo_endpoint_dependency,
    todo_id: int = Path(ge=1),
) -> None:
    """HTTP backend endpoint for retrieving a todo deletion.

    Accessible only to authenticated users.

    Args:
        user (dict): Dictionary containing user information.
        service (TodoService): A business logic layer dependency used
            to delete a todo.
        todo_id (int): The ID of the todo to be deleted.

    Returns:
        None.

    Raises:
        HTTPException: If user authentication fails or the todo item is
            not found or does not belong to the user.
    """
    service.delete(user, todo_id)
