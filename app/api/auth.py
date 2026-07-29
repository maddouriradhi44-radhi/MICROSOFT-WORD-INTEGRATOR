"""
Authentication routes.
This module exposes the register, login, and current-user
endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.enums.user_role import UserRole

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """
    # STUB: db session available but not used yet —
    # will be used once hashing + DB insert are ready
    return UserResponse(
        id=1,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=UserRole.COLLABORATOR
    )


@router.post("/login")
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate a user.
    """
    # STUB: no password check, no JWT yet
    return {
        "message": "Login endpoint",
        "email": credentials.email
    }


@router.get("/me")
def get_current_user():
    """
    Return the currently authenticated user.
    """
    # STUB: no identity check yet
    return {
        "message": "Current authenticated user."
    }