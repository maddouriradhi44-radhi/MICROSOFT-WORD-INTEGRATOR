import secrets


def generate_token() -> str:
    """
    Generate a secure random token.
    """
    return secrets.token_urlsafe(32)

