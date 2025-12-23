from fastapi import APIRouter, HTTPException, Path, status

from ..dependencies.database.db import db_dependency
from ..dependencies.user import user_dependency
from ..models import Todos
from ..schemas import TodoRequest, TodoResponse
from ..services.todo_search import find_todo

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[TodoResponse])
def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get(
    "/todo/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_model=TodoResponse,
)
async def read_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(ge=1),
):
    return find_todo(user, db, todo_id)


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: TodoRequest
):
    if user is None:
        raise HTTPException(status_code=401)
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))

    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(ge=1),
):
    todo_model = find_todo(user, db, todo_id)

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(ge=1),
):
    todo_model = find_todo(user, db, todo_id)

    db.delete(todo_model)
    db.commit()
