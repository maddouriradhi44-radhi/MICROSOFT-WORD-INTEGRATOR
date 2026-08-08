"""
Mention parser.

This module detects @mentions inside comment content.
"""

import re


def extract_mentions(content: str) -> list[str]:
    """
    Extract usernames mentioned in comment content.

    Example:
        "@Ali peux-tu vérifier cette partie ?"

    Returns:
        ["Ali"]
    """

    return re.findall(
        r"@([A-Za-z0-9_.-]+)",
        content,
    )