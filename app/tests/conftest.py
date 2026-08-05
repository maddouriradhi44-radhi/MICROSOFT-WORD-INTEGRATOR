"""
Pytest configuration.

This module provides reusable fixtures
for API testing.
"""


import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.database.session import SessionLocal



@pytest.fixture
def client():
    """
    Create a FastAPI test client.
    """

    return TestClient(app)



@pytest.fixture
def db_session():
    """
    Create a database session for tests.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()