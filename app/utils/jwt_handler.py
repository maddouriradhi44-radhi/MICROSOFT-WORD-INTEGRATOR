"""
JWT utilities.

This module provides helper functions for creating
and validating JSON Web Tokens (JWT).
"""

from datetime import datetime, timedelta

from jose import JWTError, jwt

# JWT Configuration
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to include in the token payload.
        expires_delta: Optional custom expiration time.

    Returns:
        Encoded JWT token.
    """

    to_encode = data.copy()

    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(
    token: str
) -> dict | None:
    """
    Decode and validate a JWT access token.

    Args:
        token: JWT token received from the client.

    Returns:
        The decoded payload if the token is valid,
        otherwise None.
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