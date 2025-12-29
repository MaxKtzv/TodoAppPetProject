"""Cryptographic constants and context for the application."""

from passlib.context import CryptContext

SECRET_KEY = "1215121cf2f41c6ed13c1155f077afdfee976d58cb1c8cd4d19ba2a896954b51"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
