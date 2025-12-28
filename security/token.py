from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "1215121cf2f41c6ed13c1155f077afdfee976d58cb1c8cd4d19ba2a896954b51"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

token_dependency = Annotated[str, Depends(oauth2_bearer)]


def create_access_token(
    username: str, user_id: int, whether_admin: bool, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "admin": whether_admin}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
