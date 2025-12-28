from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from ..security.token import ALGORITHM, SECRET_KEY, token_dependency


async def get_current_user(token: token_dependency):
    try:
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
