"""User Pydantic schemas.

This module defines the request and response schemas
used by the authentication API.
"""

from pydantic import BaseModel, EmailStr, ConfigDict

from app.enums.user_role import UserRole


class UserCreate(BaseModel):
    """
    Schema used to register a new user.

    The role is not provided by the client — it is assigned
    a default value at registration and can only be changed
    later by a project manager.
    """

    first_name: str
    last_name: str
    email: EmailStr

    # Plain password sent by the client — will be hashed
    # by the service before being stored, never saved as-is
    password: str

    # No "role" field on purpose: users can't pick their own role,
    # only a PROJECT_MANAGER can assign it later


class UserLogin(BaseModel):
    """
    Schema used to authenticate a user.
    """

    # Minimal schema for login — only email and password needed
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Schema returned to the client.
    """

    # What the API sends BACK to the client (register, login, profile)
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    # Role is visible here (read-only), even though the client
    # couldn't choose it in UserCreate
    role: UserRole

    # No "password" field: never return it, hashed or not

    # Lets Pydantic build this schema directly from a SQLAlchemy
    # User object (user.id, user.email, ...) instead of a dict
    model_config = ConfigDict(from_attributes=True)