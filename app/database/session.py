from sqlalchemy.orm import sessionmaker

from app.database.database import engine

# Create a session factory bound to the database engine.
# Each call to SessionLocal() will create a new Session instance
# that can be used to interact with the database.
SessionLocal = sessionmaker(
    bind=engine,       # The SQLAlchemy engine/connection this session factory will use
    autoflush=False,   # Prevents SQLAlchemy from automatically flushing pending changes
                        # to the DB before every query (gives you more control over when writes happen)
    autocommit=False   # Disables autocommit mode; you must explicitly call session.commit()
                        # to persist changes (recommended, avoids partial/unintended commits)
)