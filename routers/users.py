from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import User

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


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(User).filter(User.id == user.get("id")).first()


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    change_password_request: ChangePasswordRequest,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

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
