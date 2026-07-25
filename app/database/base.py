"""
Base class for all SQLAlchemy models.

Every ORM model in the application must inherit from this class.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all database models.
    """
    pass