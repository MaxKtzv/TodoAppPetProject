from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from ...services.admin.admin_services import AdminServices
from ...services.auth.auth_services import AuthServices
from ...services.todos.endpoint_services import TodoService
from ...services.todos.page_services import TodoPageService
from ...services.users.user_services import UserService
from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def todo_page_service(db: db_dependency):
    return TodoPageService(db)


def todo_service(db: db_dependency):
    return TodoService(db)


def get_user_service(db: db_dependency):
    return UserService(db)


def auth_service(db: db_dependency):
    return AuthServices(db)


def admin_service(db: db_dependency):
    return AdminServices(db)


todo_page_dependency = Annotated[TodoPageService, Depends(todo_page_service)]
todo_endpoint_dependency = Annotated[TodoService, Depends(todo_service)]
user_service_dependency = Annotated[UserService, Depends(get_user_service)]
auth_service_dependency = Annotated[AuthServices, Depends(auth_service)]
admin_service_dependency = Annotated[AdminServices, Depends(admin_service)]
