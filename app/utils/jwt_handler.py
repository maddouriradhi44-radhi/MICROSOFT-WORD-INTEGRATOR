"""
JWT utilities.

This module provides helper functions for:
- Access tokens
- Refresh tokens
- Email verification tokens
- Password reset tokens
"""

from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
from jose import JWTError, jwt


# ==========================================================
# Load environment variables
# ==========================================================

load_dotenv()


# ==========================================================
# JWT Configuration
# ==========================================================

SECRET_KEY = os.getenv("SECRET_KEY")

if SECRET_KEY:
    SECRET_KEY = SECRET_KEY.strip()


ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)


if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY is missing in .env file"
    )


ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "30"
    )
)


REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv(
        "REFRESH_TOKEN_EXPIRE_DAYS",
        "7"
    )
)


EMAIL_TOKEN_EXPIRE_HOURS = int(
    os.getenv(
        "EMAIL_TOKEN_EXPIRE_HOURS",
        "24"
    )
)


RESET_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "RESET_TOKEN_EXPIRE_MINUTES",
        "30"
    )
)


print("==============================")
print("JWT SECRET =", SECRET_KEY)
print("JWT ALGORITHM =", ALGORITHM)
print("==============================")



# ==========================================================
# Create Token
# ==========================================================

def create_token(
    data: dict,
    expires_delta: timedelta,
    token_type: str
) -> str:


    print("CREATE TOKEN USING SECRET =", SECRET_KEY)


    payload = data.copy()


    payload.update(
        {
            "exp": datetime.utcnow() + expires_delta,
            "type": token_type,
        }
    )


    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    return token



# ==========================================================
# Access Token
# ==========================================================

def create_access_token(
    data: dict
) -> str:

    return create_token(
        data=data,
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        token_type="access"
    )



# ==========================================================
# Refresh Token
# ==========================================================

def create_refresh_token(
    data: dict
) -> str:

    return create_token(
        data=data,
        expires_delta=timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        ),
        token_type="refresh"
    )



# ==========================================================
# Email Verification Token
# ==========================================================

def create_verification_token(
    data: dict
) -> str:

    return create_token(
        data=data,
        expires_delta=timedelta(
            hours=EMAIL_TOKEN_EXPIRE_HOURS
        ),
        token_type="verification"
    )



# ==========================================================
# Reset Password Token
# ==========================================================

def create_reset_token(
    data: dict
) -> str:

    return create_token(
        data=data,
        expires_delta=timedelta(
            minutes=RESET_TOKEN_EXPIRE_MINUTES
        ),
        token_type="reset"
    )



# ==========================================================
# Decode Token
# ==========================================================

def decode_token(
    token: str
) -> dict | None:


    if not token:
        return None


    try:

        print("DECODE TOKEN USING SECRET =", SECRET_KEY)


        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        print("JWT PAYLOAD =", payload)


        return payload


    except JWTError as e:

        print("JWT ERROR =", e)

        return None



# ==========================================================
# Decode Access Token
# ==========================================================

def decode_access_token(
    token: str
) -> dict | None:


    payload = decode_token(token)


    if payload is None:
        return None


    if payload.get("type") != "access":

        print(
            "TOKEN TYPE INVALID:",
            payload.get("type")
        )

        return None


    return payload



# ==========================================================
# Decode Refresh Token
# ==========================================================

def decode_refresh_token(
    token: str
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
    expected_type: str
) -> bool:

    return payload.get("type") == expected_type