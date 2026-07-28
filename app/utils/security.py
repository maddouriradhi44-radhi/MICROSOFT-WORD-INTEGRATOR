"""
Security utilities.

This module provides helper functions for password hashing
and password verification using bcrypt.
"""

from passlib.context import CryptContext

# Configure the password hashing algorithm (bcrypt)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.

    Args:
        password: The user's plain-text password.

    Returns:
        A securely hashed password.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    password_hash: str
) -> bool:
    """
    Verify a password against its stored hash.

    Args:
        plain_password: Password entered by the user.
        password_hash: Password hash stored in the database.

    Returns:
        True if the password is valid, otherwise False.
    """
    return pwd_context.verify(
        plain_password,
        password_hash
    )