from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.users import User
from schemas.users import UpdateUserRequest
from security.breach_checker import password_breach_check
from security.constants import bcrypt_context


class UserService:
    """Provides business logic for user endpoints.

    Attributes:
        db (Session): Database session for querying and manipulating
            data.
    """

    def __init__(self, db: Session):
        """Initialize the UserService class."""
        self.db = db

    def get(self, user: dict):
        """Retrieve user profile data.

        Args:
            user (dict): Dictionary containing user information.

        Returns:
            User: User profile data.

        Raises:
            HTTPException: If user authentication fails.
        """
        return self.db.query(User).filter(User.id == user.get("id")).first()

    def update(self, user: dict, request: UpdateUserRequest) -> None:
        """Update a user profile.

        Args:
            user (dict): Dictionary containing user information.
            request (UpdateUserRequest): The user update request schema.

        Returns:
            None

        Raises:
            HTTPException: If user authentication fails or the password
                does not match.
        """
        profile = self.get(user)
        if not bcrypt_context.verify(
            request.old_password, profile.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        password_breach_check(request.new_password)
        profile.username = request.username
        profile.email = request.email
        profile.first_name = request.first_name
        profile.last_name = request.last_name
        profile.hashed_password = bcrypt_context.hash(request.new_password)
        profile.phone_number = request.phone_number

        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
