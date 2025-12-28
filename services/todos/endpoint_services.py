from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ...models.todos import Todos


class TodoService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user):
        return (
            self.db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
        )

    def get_by_id(self, user, todo_id: int):
        todo = (
            self.db.query(Todos)
            .filter(Todos.id == todo_id, Todos.owner_id == user.get("id"))
            .first()
        )
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return todo

    def create(self, user, request):
        todo = Todos(**request.model_dump(), owner_id=user.get("id"))

        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def update(self, user, todo_id: int, request):
        todo = self.get_by_id(user, todo_id)
        todo.title = request.title
        todo.description = request.description
        todo.priority = request.priority
        todo.complete = request.complete

        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def delete(self, user, todo_id: int):
        todo = self.get_by_id(user, todo_id)

        self.db.delete(todo)
        self.db.commit()
