from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ...models.users import User
from ...security.breach_checker import password_breach_check
from ...security.token import bcrypt_context


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user):
        return self.db.query(User).filter(User.id == user.get("id")).first()

    def update(self, user, request):
        user = self.get(user)
        if not bcrypt_context.verify(
            request.old_password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        password_breach_check(request.new_password)
        user.username = request.username
        user.email = request.email
        user.first_name = request.first_name
        user.last_name = request.last_name
        user.hashed_password = bcrypt_context.hash(request.new_password)
        user.phone_number = request.phone_number

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
