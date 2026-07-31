"""
JWT utilities.

This module provides helper functions for creating
and validating JSON Web Tokens (JWT).
"""

from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
from jose import JWTError, jwt

# Load environment variables
load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7)
)

EMAIL_TOKEN_EXPIRE_HOURS = int(
    os.getenv("EMAIL_TOKEN_EXPIRE_HOURS", 24)
)

RESET_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("RESET_TOKEN_EXPIRE_MINUTES", 30)
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
        SECRET_KEY,
        algorithm=ALGORITHM
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
            SECRET_KEY,
            algorithms=[ALGORITHM]
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