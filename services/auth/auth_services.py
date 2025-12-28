from datetime import timedelta

from fastapi import HTTPException, status

from ...models.users import User
from ...security.breach_checker import password_breach_check
from ...security.token import bcrypt_context, create_access_token


class AuthServices:
    def __init__(self, db):
        self.db = db

    def check_username_and_email_uniqueness(self, create_user_request):
        existing_username = (
            self.db.query(User)
            .filter(User.username == create_user_request.username)
            .first()
        )
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

        if create_user_request.email:
            existing_email = (
                self.db.query(User)
                .filter(User.email == create_user_request.email)
                .first()
            )
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

    def authenticate_user(self, username: str, password: str):
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.hashed_password):
            return False
        return user

    def access_token(self, form_data):
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

    def create(self, create_user_request):
        self.check_username_and_email_uniqueness(create_user_request)
        password_breach_check(create_user_request.password)
        create_user_model = User(
            username=create_user_request.username,
            email=create_user_request.email,
            first_name=create_user_request.first_name,
            last_name=create_user_request.last_name,
            hashed_password=bcrypt_context.hash(create_user_request.password),
            admin=create_user_request.admin,
            is_active=True,
            phone_number=create_user_request.phone_number,
        )

        self.db.add(create_user_model)
        self.db.commit()
        self.db.refresh(create_user_model)
        return create_user_model
