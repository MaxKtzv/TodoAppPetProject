from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ...models.todos import Todos


class AdminServices:
    """Provides business logic for admin routers API endpoints.

    Attributes:
        db (Session): Database session for querying and manipulating
            data.
    """

    def __init__(self, db: Session) -> None:
        """Initialize the AdminServices class."""
        self.db = db

    def get_all_todos(self, user: dict):
        """Retrieve all todos if user is admin.

        Args:
            user (dict): The context of the authenticated admin user
                provided by the dependency.

        Returns:
            list[Todos]: A list of all todo stored in the database.

        Raises:
            HTTPException: If admin authentication fails.
        """
        if not user.get("admin"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return self.db.query(Todos).all()

    def delete(self, user: dict, todo_id: int) -> None:
        """Delete todo by ID if user is admin.

        Args:
            user (dict): The context of the authenticated admin user
                provided by the dependency.
            todo_id (int): The ID of the todo to be deleted.

        Returns:
            None

        Raises:
            HTTPException: If admin authentication fails.
        """
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
