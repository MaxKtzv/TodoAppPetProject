from sqlalchemy import Boolean, Column, Integer, String

from dependencies.database.database import Base


class User(Base):
    """SQLAlchemy model for representing a user in the database."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    admin = Column(Boolean, default=False, nullable=False)
