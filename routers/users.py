"""A collection of user-related backend APIs for managing user profile."""

from fastapi import APIRouter, status

from dependencies.current_user import user_dependency
from dependencies.database.db import user_service_dependency
from schemas.users import UpdateUserRequest, UserResponse

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user: user_dependency, service: user_service_dependency):
    """HTTP backend endpoint for retrieving user profile data.

    Args:
        user (dict): Dictionary containing user information.
        service (UserService): A business logic layer dependency used
            to retrieve user profile data.

    Returns:
        UserResponse: User profile data.

    Raises:
        HTTPException: If user authentication fails.
    """
    return service.get(user)


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_profile(
    user: user_dependency,
    request: UpdateUserRequest,
    service: user_service_dependency,
) -> None:
    """HTTP backend endpoint for updating a user profile.

    Args:
        user (dict): Dictionary containing user information.
        request (UpdateUserRequest): The user update request schema.
        service (UserService): A business logic layer dependency used
            to update a user profile.

    Returns:
        None

    Raises:
        HTTPException: If user authentication fails or the password does
            not match.
    """
    service.update(user, request)
