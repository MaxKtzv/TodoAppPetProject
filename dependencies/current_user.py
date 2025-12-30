"""Dependencies for authenticating and retrieving current user data."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from security.constants import ALGORITHM, SECRET_KEY

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

token_dependency = Annotated[str, Depends(oauth2_bearer)]


async def get_current_user(token: token_dependency) -> dict:
    """Retrieve the current user information from a JWT token.

    The token is decoded to extract user data such as username, user
    ID, and administrative permissions.

    Args:
        token: The token obtained from dependencies that is used to
            authenticate the user.

    Returns:
        dict: A dictionary containing the user's username, ID, and admin
            status.

    Raises:
        HTTPException: Raised when the token is invalid or does not
            contain the required credentials.
    """
    try:
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        is_admin: bool = payload.get("admin")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return {"username": username, "id": user_id, "admin": is_admin}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


user_dependency = Annotated[dict, Depends(get_current_user)]
