feature/database-models
"""
Database session configuration.

This module creates a session factory that will be used
to interact with the PostgreSQL database.

Each call to SessionLocal() creates a new database session.
"""

 main
from sqlalchemy.orm import sessionmaker

from app.database.database import engine

# Create a session factory bound to the database engine.
 feature/database-models
# Every session created by SessionLocal() will use the same engine.
SessionLocal = sessionmaker(
    bind=engine,

    # Disable automatic flushing.
    # Changes are sent to the database only when explicitly requested.
    autoflush=False,

    # Disable automatic commits.
    # Every transaction must be committed manually using session.commit().
    autocommit=False,

# Each call to SessionLocal() will create a new Session instance
# that can be used to interact with the database.
SessionLocal = sessionmaker(
    bind=engine,       # The SQLAlchemy engine/connection this session factory will use
    autoflush=False,   # Prevents SQLAlchemy from automatically flushing pending changes
                        # to the DB before every query (gives you more control over when writes happen)
    autocommit=False   # Disables autocommit mode; you must explicitly call session.commit()
                        # to persist changes (recommended, avoids partial/unintended commits)
main
)