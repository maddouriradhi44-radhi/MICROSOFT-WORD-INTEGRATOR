"""
Authentication routes.

This module exposes the authentication endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    created_user = AuthService.register(
        user_data=user,
        db=db,
    )

    return created_user


@router.post("/login")
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticate a user.
    """

    return AuthService.login(
        email=credentials.email,
        password=credentials.password,
        db=db,
    )


@router.get("/verify-email")
def verify_email(
    token: str,
    db: Session = Depends(get_db),
):
    """
    Verify a user's email.
    """

    return AuthService.verify_email(
        token=token,
        db=db,
    )


@router.get("/me")
def get_current_user():
    """
    Return the currently authenticated user.

    (Will be implemented after JWT authentication.)
    """

    return {
        "message": "Current authenticated user."
    }