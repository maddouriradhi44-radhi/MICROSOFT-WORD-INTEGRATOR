"""
Database engine configuration.

This module creates the SQLAlchemy engine,
which is responsible for connecting to the PostgreSQL database.
"""

from sqlalchemy import create_engine

from app.config import DATABASE_URL

# Create the SQLAlchemy engine.
# The engine manages connections to the PostgreSQL database.
engine = create_engine(
    DATABASE_URL,

    # Display all generated SQL queries in the console.
    # Useful during development and debugging.
    echo=True,
)