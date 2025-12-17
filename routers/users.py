from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import User
from services.breach_checker import password_breach_check

from .auth import bcrypt_context, get_current_user

router = APIRouter(prefix="/user", tags=["user"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class ChangePhoneRequest(BaseModel):
    phone_number: str


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(User).filter(User.id == user.get("id")).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    change_password_request: ChangePasswordRequest,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    breached_password = password_breach_check(change_password_request.password)
    if breached_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password found in a breach — try another.",
        )

    user_model = db.query(User).filter(User.id == user.get("id")).first()
    if not bcrypt_context.verify(
        change_password_request.old_password, user_model.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Incorrect old password")
    user_model.hashed_password = bcrypt_context.hash(
        change_password_request.new_password
    )
    db.add(user_model)
    db.commit()


@router.put("/phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    phone_number: str,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(User).filter(User.id == user.get("id")).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
