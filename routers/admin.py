from fastapi import APIRouter, Path, status

from ..dependencies.current_user import user_dependency
from ..dependencies.database.db import admin_service_dependency

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_todos(user: user_dependency, service: admin_service_dependency):
    return service.get_all_todos(user)


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    service: admin_service_dependency,
    todo_id: int = Path(ge=1),
):
    return service.delete(user, todo_id)
