"""Database dependency configuration utilities."""

from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies.database.database import SessionLocal
from services.admin.admin_services import AdminServices
from services.auth.auth_services import AuthServices
from services.todos.backend_services import TodoService
from services.todos.frontend_services import TodoPageService
from services.users.user_services import UserService


def get_db() -> Generator[Session]:
    """Database session generator.

    A context manager for managing database sessions. Ensures that a
    session is properly opened and closed after its use.

    Yields:
        Session: A new database session object for carrying out database
            operations.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def todo_page_service(db: db_dependency) -> TodoPageService:
    """Provide database dependency to TodoPageService.

    Args:
        db (Session): Database dependency.

    Returns:
        TodoPageService: A database initialized instance of
            TodoPageService.
    """
    return TodoPageService(db)


def todo_service(db: db_dependency) -> TodoService:
    """Provide database dependency to TodoService.

    Args:
        db (Session): Database dependency.

    Returns:
        TodoService: A database initialized instance of TodoService.
    """
    return TodoService(db)


def get_user_service(db: db_dependency) -> UserService:
    """Provide database dependency to UserService.

    Args:
        db (Session): Database dependency.

    Returns:
        UserService: A database initialized instance of UserService.
    """
    return UserService(db)


def auth_service(db: db_dependency) -> AuthServices:
    """Provide database dependency to AuthServices.

    Args:
        db (Session): Database dependency.

    Returns:
        AuthServices: A database initialized instance of AuthServices.
    """
    return AuthServices(db)


def admin_service(db: db_dependency) -> AdminServices:
    """Provide database dependency to AdminServices.

    Args:
        db (Session): Database dependency.

    Returns:
        AdminServices: A database initialized instance of AdminServices.
    """
    return AdminServices(db)


todo_page_dependency = Annotated[TodoPageService, Depends(todo_page_service)]
todo_endpoint_dependency = Annotated[TodoService, Depends(todo_service)]
user_service_dependency = Annotated[UserService, Depends(get_user_service)]
auth_service_dependency = Annotated[AuthServices, Depends(auth_service)]
admin_service_dependency = Annotated[AdminServices, Depends(admin_service)]
