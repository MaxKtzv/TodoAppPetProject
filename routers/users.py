from fastapi import APIRouter, HTTPException, status

from ..dependencies.database.db import db_dependency
from ..dependencies.user import bcrypt_context, user_dependency
from ..models import User
from ..schemas import ChangePasswordRequest, UserResponse
from ..services.breach_checker import password_breach_check

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db.query(User).filter(User.id == user.get("id")).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    change_password_request: ChangePasswordRequest,
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    password_breach_check(change_password_request.new_password)
    user_model = db.query(User).filter(User.id == user.get("id")).first()
    if not bcrypt_context.verify(
        change_password_request.old_password, user_model.hashed_password
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_model.hashed_password = bcrypt_context.hash(
        change_password_request.new_password
    )
    db.add(user_model)
    db.commit()


@router.put("/phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    user: user_dependency,
    db: db_dependency,
    phone_number: int,
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_model = db.query(User).filter(User.id == user.get("id")).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
