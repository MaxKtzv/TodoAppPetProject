from datetime import datetime, timedelta, timezone

from jose import jwt

from .constants import ALGORITHM, SECRET_KEY


def create_access_token(
    username: str, user_id: int, whether_admin: bool, expires_delta: timedelta
) -> str:
    """Generates a JSON Web Token (JWT) for authentication.

    The token encodes username, user ID, and admin status.

    Args:
        username (str): The username of the user.
        user_id (int): A unique identifier for the user.
        whether_admin (bool): Specifies whether the user has
            administrative privileges.
        expires_delta (timedelta): The time duration after which the
            token expires.

    Returns:
        str: A JWT string encoded using the specified secret key and
            HS256 algorithm.
    """
    encode = {"sub": username, "id": user_id, "admin": whether_admin}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
