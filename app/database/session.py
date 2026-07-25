"""
Database session configuration.

This module creates a session factory that will be used
to interact with the PostgreSQL database.

Each call to SessionLocal() creates a new database session.
"""

from sqlalchemy.orm import sessionmaker

from app.database.database import engine

# Create a session factory bound to the database engine.
# Every session created by SessionLocal() will use the same engine.
SessionLocal = sessionmaker(
    bind=engine,

    # Disable automatic flushing.
    # Changes are sent to the database only when explicitly requested.
    autoflush=False,

    # Disable automatic commits.
    # Every transaction must be committed manually using session.commit().
    autocommit=False,
)