"""Provide test environment, dependencies, configuration, and utilities."""

from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from dependencies.current_user import get_current_user
from dependencies.database.database import Base
from dependencies.database.db import get_db
from main import app
from models.todos import Todos
from models.users import User
from security.constants import bcrypt_context

SQLITE_FILE_PATH = Path(__file__).resolve().with_name("testdb.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{SQLITE_FILE_PATH.as_posix()}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator[Session]:
    """Database session generator for testing.

    Ensures that a session is properly opened and closed after its use.

    Yields:
        Session: A new database session object for carrying out database
            operations.
    """
    db: Session = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user() -> dict:
    """Provides mock user details for testing.

    Returns:
        dict: Mock user details.
    """
    return {
        "username": "test_admin",
        "id": 1,
        "admin": True,
    }


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_todo() -> Generator[Todos]:
    """Pre-seeded todo data instance for testing.

    Yields:
        Todos: A Todos model instance.
    """
    todo = Todos(
        id=1,
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db: Session = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user() -> Generator[User]:
    """Pre-seeded user data instance for testing.

    Yields:
        User: A User model instance.
    """
    user = User(
        username="test_admin",
        email="test@email.com",
        first_name="Test",
        last_name="User",
        hashed_password=bcrypt_context.hash("test_password"),
        admin=True,
        phone_number="+1 (123) 456-7890",
    )
    db: Session = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
