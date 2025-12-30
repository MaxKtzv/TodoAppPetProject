from datetime import timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models.users import User
from schemas.users import CreateUserRequest
from security.breach_checker import password_breach_check
from security.constants import bcrypt_context
from security.token import create_access_token


class AuthServices:
    """Provides business logic for authentication endpoints.

    Attributes:
        db (Session): Database session for querying and manipulating
            data.
    """

    def __init__(self, db: Session):
        """Initialize the AuthServices class."""
        self.db = db

    def check_username_and_email_uniqueness(
        self, request: CreateUserRequest
    ) -> None:
        """Check the uniqueness of the username and email address.

        Args:
            request: The request object containing username and email
                to be verified for uniqueness.

        Returns:
            None.

        Raises:
            HTTPException: If the username is already taken or if the
                email is already registered.
        """
        existing_username = (
            self.db.query(User)
            .filter(User.username == request.username)
            .first()
        )
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

        if request.email:
            existing_email = (
                self.db.query(User).filter(User.email == request.email).first()
            )
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

    def authenticate_user(self, username: str, password: str):
        """Authenticate the user by comparing credentials.

        Args:
            username (str): The username string.
            password (str): The password string.

        Returns:
            user (User) | bool: The authenticated User object if
                credentials match, otherwise False.
        """
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.hashed_password):
            return False
        return user

    def access_token(self, form_data: OAuth2PasswordRequestForm) -> dict:
        """Generate an access token for the authenticated users.

        Args:
            form_data (OAuth2PasswordRequestForm): The user credentials
                (username and password) provided in the request.

        Returns:
            dict: The access token and its type.

        Raises:
            HTTPException: If authentication fails.
        """
        user = self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        token = create_access_token(
            user.username, user.id, user.admin, timedelta(minutes=20)
        )
        return {"access_token": token, "token_type": "bearer"}

    def create(self, request: CreateUserRequest) -> None:
        """Creates a new user in the database with the given details.

        The method ensures uniqueness of the username and email
        provided, verifies the strength and safety of the password
        and hashes it before being stored.

        Args:
            request (CreateUserRequest): An instance of
                CreateUserRequest containing the details for the
                new user.

        Returns:
            None
        """
        self.check_username_and_email_uniqueness(request)
        password_breach_check(request.password)
        user = User(
            username=request.username,
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            hashed_password=bcrypt_context.hash(request.password),
            admin=request.admin,
            is_active=True,
            phone_number=request.phone_number,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
