"""
Permission exceptions.

Custom exceptions related to authorization.
"""


class PermissionDeniedException(Exception):
    """
    Raised when a user does not have
    permission to perform an action.
    """

    def __init__(self):
        super().__init__(
            "You do not have permission to perform this action."
        )