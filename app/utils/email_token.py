"""
Email token utilities.

This module provides functions to generate secure tokens
used for email verification and password reset.
"""

import secrets


def generate_email_token() -> str:
    """
    Generate a secure random token for email verification.

    Returns:
        str: A URL-safe random token.
    """
    return secrets.token_urlsafe(32)


def generate_password_reset_token() -> str:
    """
    Generate a secure random token for password reset.

    Returns:
        str: A URL-safe random token.
    """
    return secrets.token_urlsafe(32)