"""Database connection and configuration using SQLAlchemy."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLITE_FILE_PATH = Path(__file__).resolve().with_name("todoapp.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{SQLITE_FILE_PATH.as_posix()}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
