"""
User repository.

This module contains all database operations
related to the User model.

By centralizing database queries in one place,
the code becomes easier to maintain, test,
and extend over time.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ) -> User | None:
        """
        Return a user by email.

        Returns None if no user exists.
        """

        result = db.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    @staticmethod
    def create(
    db: Session,
    user: User
    ) -> User:
        """
    Save a new user to the database.

    Args:
        db: Active database session.
        user: User instance to save.

    Returns:
        The saved User instance.
     """

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    @staticmethod
    def get_by_id(
    db: Session,
            user_id: int
    ) -> User | None:
        """
    Return a user by id.

    Returns None if no user exists.
    """

        result = db.execute(
        select(User).where(User.id == user_id)
    )

        return result.scalar_one_or_none()

    @staticmethod
    def update(
        db: Session,
        user: User
    ) -> User:
        """
        Update an existing user.

        Returns:
            The updated User instance.
        """

        db.commit()
        db.refresh(user)
        return user
    @staticmethod
    def get_by_verification_token(
        db: Session,
        token: str
    ):
        """
     Find user by email verification token.
         """

        result = db.execute(
            select(User).where(
              User.verification_token == token
             )
     )

        return result.scalar_one_or_none()

    @staticmethod
    def get_by_reset_token(
        db: Session,
        token: str
    ):

        result = db.execute(
             select(User).where(
             User.reset_token == token
            )
        )

        return result.scalar_one_or_none()
        
   