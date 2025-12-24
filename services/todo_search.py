from fastapi import HTTPException, status

from ..models import Todos


def find_todo(user, db, todo_id):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return todo_model
