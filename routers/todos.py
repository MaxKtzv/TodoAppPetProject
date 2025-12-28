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
    return await service.get_page(request)


@router.get("/add-todo-page")
async def add_todos_page(request: Request, service: todo_page_dependency):
    return await service.add_page(request)


@router.get("/edit-todo-page/{todo_id}", status_code=status.HTTP_200_OK)
async def edit_todos_page(
    request: Request,
    service: todo_page_dependency,
    todo_id: int = Path(ge=1),
):
    return await service.edit_page(request, todo_id)


### Endpoints ###
@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[TodoResponse]
)
def read_all(user: user_dependency, service: todo_endpoint_dependency):
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
    return service.get_by_id(user, todo_id)


@router.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(
    user: user_dependency,
    request: TodoRequest,
    service: todo_endpoint_dependency,
):
    service.create(user, request)


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(
    user: user_dependency,
    request: TodoRequest,
    service: todo_endpoint_dependency,
    todo_id: int = Path(ge=1),
):
    service.update(user, todo_id, request)


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    user: user_dependency,
    service: todo_endpoint_dependency,
    todo_id: int = Path(ge=1),
):
    service.delete(user, todo_id)
