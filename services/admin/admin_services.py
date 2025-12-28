from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ...models.todos import Todos


class AdminServices:
    def __init__(self, db: Session):
        self.db = db

    def get_all_todos(self, user):
        if not user.get("admin"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return self.db.query(Todos).all()

    def delete(self, user, todo_id):
        if not user.get("admin"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        todo_model = self.db.query(Todos).filter(Todos.id == todo_id).first()
        if todo_model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        self.db.delete(todo_model)
        self.db.commit()
