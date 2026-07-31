"""
Email validation utilities.

This module verifies if an email address
belongs to an authorized domain.
"""

from fastapi import HTTPException, status


ALLOWED_EMAIL_DOMAINS = [
    "capgemini.com"
]


def validate_email_domain(email: str) -> None:
    """
    Verify that email domain is authorized.

    Raises:
        HTTPException: if domain is not allowed.
    """

    domain = email.split("@")[-1].lower()

    if domain not in ALLOWED_EMAIL_DOMAINS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email domain is not authorized."
        )