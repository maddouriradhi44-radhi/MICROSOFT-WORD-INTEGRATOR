"""
Authentication service.

Contains the business logic for:

- Register
- Login
- Email verification
"""

import os
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums.user_role import UserRole
from app.models.user import User
from app.services.email_service import send_verification_email

from app.utils.security import (
    hash_password,
    verify_password,
    validate_password,
)

from app.utils.jwt_handler import (
    create_access_token,
    create_refresh_token,
    create_verification_token,
)


class AuthService:
    """
    Authentication business logic.
    """

    @staticmethod
    def register(user_data, db: Session) -> User:
        """
        Register a new user.
        """

        # Check if email already exists
        existing_user = (
            db.query(User)
            .filter(User.email == user_data.email)
            .first()
        )

        if existing_user:
            raise ValueError("Email already registered.")

        # Restrict email domain
        allowed_domain = os.getenv("ALLOWED_EMAIL_DOMAINS")

        if (
            allowed_domain
            and not user_data.email.lower().endswith(
                f"@{allowed_domain.lower()}"
            )
        ):
            raise ValueError(
                f"Only {allowed_domain} email addresses are allowed."
            )

        # Validate password
        if not validate_password(user_data.password):
            raise ValueError(
                "Password does not meet security requirements."
            )

        password_hash = hash_password(user_data.password)

        verification_token = create_verification_token(
            {
                "email": user_data.email,
            }
        )

        verification_token_expires = (
            datetime.utcnow() + timedelta(hours=24)
        )

        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password_hash=password_hash,
            role=UserRole.COLLABORATOR,
            is_verified=False,
            verification_token=verification_token,
            verification_token_expires=verification_token_expires,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        send_verification_email(
            email=user.email,
            token=verification_token,
        )

        return user

    @staticmethod
    def login(
        email: str,
        password: str,
        db: Session,
    ) -> dict:
        """
        Authenticate a user and generate JWT tokens.
        """

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if user is None:
            raise ValueError("Invalid email or password.")

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise ValueError("Invalid email or password.")

        if not user.is_verified:
            raise ValueError(
                "Please verify your email before logging in."
            )

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user,
        }

    @staticmethod
    def verify_email(
        token: str,
        db: Session,
    ) -> dict:
        """
        Verify a user's email address.
        """

        user = (
            db.query(User)
            .filter(User.verification_token == token)
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification token.",
            )

        if user.verification_token_expires is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification token is invalid.",
            )

        if datetime.utcnow() > user.verification_token_expires:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification token has expired.",
            )

        user.is_verified = True
        user.verification_token = None
        user.verification_token_expires = None

        db.commit()
        db.refresh(user)

        return {
            "message": "Email verified successfully."
        }