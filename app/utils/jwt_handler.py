"""
JWT utilities.

This module provides helper functions for:
- Access tokens
- Refresh tokens
- Email verification tokens
- Password reset tokens
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


# ==========================================================
# Create Token
# ==========================================================

def create_token(
    data: dict,
    expires_delta: timedelta,
    token_type: str,
) -> str:

    print("CREATE TOKEN USING SECRET =", JWT_SECRET_KEY)

    payload = data.copy()

    payload.update(
        {
            "exp": datetime.utcnow() + expires_delta,
            "type": token_type,
        }
    )

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    return token


# ==========================================================
# Access Token
# ==========================================================

def create_access_token(
    data: dict,
) -> str:

    return create_token(
        data=data,
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        token_type="access",
    )


# ==========================================================
# Refresh Token
# ==========================================================

def create_refresh_token(
    data: dict,
) -> str:

    return create_token(
        data=data,
        expires_delta=timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        ),
        token_type="refresh",
    )


# ==========================================================
# Email Verification Token
# ==========================================================

def create_verification_token(
    data: dict,
) -> str:

    return create_token(
        data=data,
        expires_delta=timedelta(
            hours=EMAIL_TOKEN_EXPIRE_HOURS
        ),
        token_type="verification",
    )


# ==========================================================
# Reset Password Token
# ==========================================================

def create_reset_token(
    data: dict,
) -> str:

    return create_token(
        data=data,
        expires_delta=timedelta(
            minutes=RESET_TOKEN_EXPIRE_MINUTES
        ),
        token_type="reset",
    )


# ==========================================================
# Decode Token
# ==========================================================

def decode_token(
    token: str,
) -> dict | None:

    if not token:
        return None

    try:

        print(
            "DECODE TOKEN USING SECRET =",
            JWT_SECRET_KEY
        )

        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        print(
            "JWT PAYLOAD =",
            payload
        )

        return payload

    except JWTError as e:

        print(
            "JWT ERROR =",
            e
        )

        return None


# ==========================================================
# Decode Access Token
# ==========================================================

def decode_access_token(
    token: str,
) -> dict | None:

    payload = decode_token(token)

    if payload is None:
        return None

    if payload.get("type") != "access":
        return None

    return payload


# ==========================================================
# Decode Refresh Token
# ==========================================================

def decode_refresh_token(
    token: str,
) -> dict | None:

    payload = decode_token(token)

    if payload is None:
        return None

    if payload.get("type") != "refresh":
        return None

    return payload


# ==========================================================
# Validate Token Type
# ==========================================================

def validate_token_type(
    payload: dict,
    expected_type: str,
) -> bool:

    return payload.get("type")