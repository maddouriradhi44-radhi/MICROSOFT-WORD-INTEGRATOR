"""
JWT utilities.

This module provides helper functions for creating
and validating JSON Web Tokens (JWT).
"""

from datetime import datetime, timedelta

from jose import jwt, JWTError

from app.config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    EMAIL_TOKEN_EXPIRE_HOURS,
    RESET_TOKEN_EXPIRE_MINUTES,
)


def create_token(
    data: dict,
    expires_delta: timedelta,
    token_type: str
) -> str:
    """
    Create a generic JWT token.

    Args:
        data: Payload to encode.
        expires_delta: Token lifetime.
        token_type: access, refresh, verification or reset.

    Returns:
        Encoded JWT token.
    """

    payload = data.copy()

    payload.update(
        {
            "exp": datetime.utcnow() + expires_delta,
            "type": token_type
        }
    )

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )


def create_access_token(data: dict) -> str:
    """
    Create an access token.
    """

    return create_token(
        data=data,
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        token_type="access"
    )


def create_refresh_token(data: dict) -> str:
    """
    Create a refresh token.
    """

    return create_token(
        data=data,
        expires_delta=timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        ),
        token_type="refresh"
    )


def create_verification_token(data: dict) -> str:
    """
    Create an email verification token.
    """

    return create_token(
        data=data,
        expires_delta=timedelta(
            hours=EMAIL_TOKEN_EXPIRE_HOURS
        ),
        token_type="verification"
    )


def create_reset_token(data: dict) -> str:
    """
    Create a password reset token.
    """

    return create_token(
        data=data,
        expires_delta=timedelta(
            minutes=RESET_TOKEN_EXPIRE_MINUTES
        ),
        token_type="reset"
    )


def decode_token(
    token: str
) -> dict | None:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token.

    Returns:
        Decoded payload if valid, otherwise None.
    """

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
        return payload

    except JWTError:
        return None


def validate_token_type(
    payload: dict,
    expected_type: str
) -> bool:
    """
    Validate the token type.

    Args:
        payload: Decoded JWT payload.
        expected_type: Expected token type.

    Returns:
        True if the token type matches.
    """

    return payload.get("type") == expected_type

def decode_access_token(token: str):
    """
    Decode and verify a JWT access token.
    """

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        return payload

    except JWTError:
        return None