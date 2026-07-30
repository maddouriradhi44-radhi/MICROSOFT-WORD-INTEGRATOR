"""
Authentication service.

This module contains the business logic
related to user authentication.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.enums.user_role import UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token,
)
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import create_access_token


class AuthService:
    """
    Service responsible for authentication
    and user account management.
    """

    @staticmethod
    def register(
        db: Session,
        user_data: UserCreate
    ) -> UserResponse:
        """
        Register a new user.

        This method will:
        - Check if the email already exists.
        - Hash the password.
        - Create a new user.
        - Save it to the database.
        - Return the created user.
        """

        existing_user = UserRepository.get_by_email(
            db,
            user_data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered."
            )

        hashed_password = hash_password(user_data.password)

        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password_hash=hashed_password,
            role=UserRole.COLLABORATOR
        )

        created_user = UserRepository.create(db, new_user)

        # Register renvoie l'utilisateur créé, PAS un token —
        # l'utilisateur doit ensuite se connecter via /login
        return UserResponse.model_validate(created_user)

    @staticmethod
    def login(
        db: Session,
        credentials: UserLogin
    ) -> Token:
        """
        Authenticate a user and return a JWT access token.
        """

        user = UserRepository.get_by_email(
            db,
            credentials.email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        if not verify_password(
            credentials.password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        # Login génère et renvoie le token JWT
        token = create_access_token(
            {"sub": user.email}
        )

        return Token(
            access_token=token,
            token_type="bearer"
        )

    @staticmethod
    def get_current_user(
        db: Session,
        email: str
    ) -> UserResponse:
        """
        Return the currently authenticated user.
        """


        user = UserRepository.get_by_email(
            db,
            email
        )


        if not user:
            raise Exception(
                "User not found"
            )


        return UserResponse.model_validate(
            user
        )