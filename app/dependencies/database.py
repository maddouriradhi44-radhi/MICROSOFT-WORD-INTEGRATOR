"""
Database dependency.

This module provides the database session dependency
used by FastAPI endpoints.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session for each request.

    The session is automatically closed after
    the request has been processed.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
        