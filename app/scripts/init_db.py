"""
Database initialization script.

This script creates all database tables
defined by the SQLAlchemy models.
"""

from app.database.base import Base
from app.database.database import engine

# Import all models so SQLAlchemy registers them
from app.models import *


def initialize_database() -> None:
    """
    Create all database tables.
    """

    print("=" * 50)
    print("Creating database tables...")
    print("=" * 50)

    Base.metadata.create_all(bind=engine)

    print("=" * 50)
    print("Database initialized successfully!")
    print("=" * 50)


if __name__ == "__main__":
    initialize_database()