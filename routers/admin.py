from fastapi import APIRouter, HTTPException, Path, status

from ..dependencies.database.db import db_dependency
from ..dependencies.user import user_dependency
from ..models import Todos

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_todos(user: user_dependency, db: db_dependency):
    if not user.get("admin"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(ge=1)
):
    if not user.get("admin"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(todo_model)
    db.commit()
