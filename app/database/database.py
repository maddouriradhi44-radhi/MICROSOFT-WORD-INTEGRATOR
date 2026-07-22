from sqlalchemy import create_engine
from app.config import DATABASE_URL
# Create the SQLAlchemy engine using the database URL
engine = create_engine(
    # Database connection URL loaded from the configuration file
    DATABASE_URL,

    # Display all generated SQL queries in the console (useful for debugging)
    echo=True
)

