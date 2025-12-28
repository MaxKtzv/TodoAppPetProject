from fastapi import APIRouter, status

from ..dependencies.current_user import user_dependency
from ..dependencies.database.db import user_service_dependency
from ..schemas.users import UpdateUserRequest, UserResponse

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user: user_dependency, service: user_service_dependency):
    return service.get(user)


@router.put("/profile", status_code=status.HTTP_204_NO_CONTENT)
async def update_profile(
    user: user_dependency,
    request: UpdateUserRequest,
    service: user_service_dependency,
):
    return service.update(user, request)
