"""
Authentication service.

This module contains the business logic
related to user authentication.
"""

import time
from datetime import datetime, timedelta

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
from app.utils.email_token import generate_email_token
from app.utils.email_validator import validate_email_domain
from app.utils.token_generator import generate_token
from app.services.email_service import EmailService
from app.services.notifications_service import NotificationService
from app.enums.notification_type import NotificationType
from app.enums.notification_level import NotificationLevel
from app.services.audit_log_service import AuditLogService
from app.enums.audit_action import AuditAction


notification_service = NotificationService()
audit_log_service = AuditLogService()

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

        validate_email_domain(
            user_data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered."
            )

        hashed_password = hash_password(user_data.password)
        verification_token = generate_email_token()
        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password_hash=hashed_password,
            role=UserRole.COLLABORATOR,
            is_verified=False,
            verification_token=verification_token
        )

        created_user = UserRepository.create(db, new_user)

        EmailService.send_verification_email(
            created_user.email,
            created_user.verification_token
        )

        notification_service.notify_user(
            db=db,
            user_id=created_user.id,
            title="Account Created",
            message="Your account has been created successfully. Please verify your email address.",
            notification_type=NotificationType.SECURITY,
            level=NotificationLevel.SUCCESS,
        )

        audit_log_service.log_action(
            db=db,
            user_id=created_user.id,
            action=AuditAction.CREATE,
            target=f"user:{created_user.id}",
        )

        return UserResponse.model_validate(created_user)

    @staticmethod
    def login(
        db: Session,
        credentials: UserLogin
    ) -> Token:
        """
        Authenticate a user and return a JWT access token.
        Temporary performance instrumentation.
        """

        total_start = time.perf_counter()

        # ---------------------------------------------------------
        # 1. Recherche utilisateur
        # ---------------------------------------------------------

        start = time.perf_counter()

        user = UserRepository.get_by_email(
            db,
            credentials.email
        )

        print(
            f"[AUTH LOGIN] get_by_email: "
            f"{time.perf_counter() - start:.3f}s"
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        # ---------------------------------------------------------
        # 2. Vérification email
        # ---------------------------------------------------------

        start = time.perf_counter()

        if not user.is_verified:
            print(
                f"[AUTH LOGIN] is_verified check: "
                f"{time.perf_counter() - start:.3f}s"
            )

            notification_service.notify_user(
                db=db,
                user_id=user.id,
                title="Unverified Login Attempt",
                message=(
                    "A login attempt was made while your email "
                    "address is not verified."
                ),
                notification_type=NotificationType.SECURITY,
                level=NotificationLevel.WARNING,
            )

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not verified."
            )

        print(
            f"[AUTH LOGIN] is_verified check: "
            f"{time.perf_counter() - start:.3f}s"
        )

        # ---------------------------------------------------------
        # 3. Vérification bcrypt
        # ---------------------------------------------------------

        start = time.perf_counter()

        password_valid = verify_password(
            credentials.password,
            user.password_hash
        )

        print(
            f"[AUTH LOGIN] verify_password: "
            f"{time.perf_counter() - start:.3f}s"
        )

        if not password_valid:

            start = time.perf_counter()

            notification_service.notify_user(
                db=db,
                user_id=user.id,
                title="Failed Login Attempt",
                message=(
                    "A failed login attempt was detected "
                    "on your account."
                ),
                notification_type=NotificationType.SECURITY,
                level=NotificationLevel.WARNING,
            )

            print(
                f"[AUTH LOGIN] failed notification: "
                f"{time.perf_counter() - start:.3f}s"
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        # ---------------------------------------------------------
        # 4. Génération JWT
        # ---------------------------------------------------------

        start = time.perf_counter()

        token = create_access_token(
            {"sub": user.email}
        )

        print(
            f"[AUTH LOGIN] create_access_token: "
            f"{time.perf_counter() - start:.3f}s"
        )

        # ---------------------------------------------------------
        # 6. Audit login
        # ---------------------------------------------------------

        start = time.perf_counter()

        audit_log_service.log_action(
            db=db,
            user_id=user.id,
            action=AuditAction.LOGIN,
            target=f"user:{user.id}",
        )

        print(
            f"[AUTH LOGIN] audit log: "
            f"{time.perf_counter() - start:.3f}s"
        )

        # ---------------------------------------------------------
        # 7. Total
        # ---------------------------------------------------------

        print(
            f"[AUTH LOGIN] TOTAL: "
            f"{time.perf_counter() - total_start:.3f}s"
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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserResponse.model_validate(user)

    @staticmethod
    def verify_email(
        db: Session,
        token: str
    ) -> dict:
        """
        Verify user account using email token.
        """

        user = UserRepository.get_by_verification_token(
            db,
            token
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification token."
            )

        if (
            user.verification_token_expires
            and user.verification_token_expires < datetime.utcnow()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification token expired."
            )

        user.is_verified = True
        user.verification_token = None
        user.verification_token_expires = None

        db.commit()
        db.refresh(user)

        notification_service.notify_user(
            db=db,
            user_id=user.id,
            title="Email Verified",
            message="Your email address has been successfully verified.",
            notification_type=NotificationType.SECURITY,
            level=NotificationLevel.SUCCESS,
        )

        audit_log_service.log_action(
            db=db,
            user_id=user.id,
            action=AuditAction.VERIFY_EMAIL,
            target=f"user:{user.id}",
        )

        return {
            "message": "Email verified successfully."
        }

    @staticmethod
    def forgot_password(
        db: Session,
        email: str
    ) -> dict:
        """
        Generate a password reset token and send it by email.
        """

        user = UserRepository.get_by_email(
            db,
            email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not email.endswith("@capgemini.com"):
            raise HTTPException(
                status_code=400,
                detail="Only @capgemini.com emails are allowed"
            )

        reset_token = generate_token()

        user.reset_token = reset_token
        user.reset_token_expires = (
            datetime.utcnow() + timedelta(minutes=30)
        )

        db.commit()
        db.refresh(user)

        EmailService.send_reset_password_email(
            user.email,
            reset_token
        )

        notification_service.notify_user(
            db=db,
            user_id=user.id,
            title="Password Reset Requested",
            message="A password reset request has been made for your account.",
            notification_type=NotificationType.SECURITY,
            level=NotificationLevel.WARNING,
        )

        return {
            "message": "Password reset email sent."
        }

    @staticmethod
    def reset_password(
        db: Session,
        token: str,
        new_password: str
    ) -> dict:
        """
        Reset password using a valid reset token.
        """

        user = db.query(User).filter(
            User.reset_token == token
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token"
            )

        if (
            user.reset_token_expires
            and user.reset_token_expires < datetime.utcnow()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token expired"
            )

        user.password_hash = hash_password(new_password)
        user.reset_token = None
        user.reset_token_expires = None

        db.commit()
        db.refresh(user)

        notification_service.notify_user(
            db=db,
            user_id=user.id,
            title="Password Changed",
            message="Your password has been successfully changed.",
            notification_type=NotificationType.SECURITY,
            level=NotificationLevel.SUCCESS,
        )

        return {
            "message": "Password successfully changed"
        }

    @staticmethod
    def logout(
        db: Session,
        user: User,
    ) -> dict:
        """
        Logout the authenticated user and record the action
        in the audit log.
        """

        audit_log_service.log_action(
            db=db,
            user_id=user.id,
            action=AuditAction.LOGOUT,
            target=f"user:{user.id}",
        )

        return {
            "message": "Logout successful."
        }