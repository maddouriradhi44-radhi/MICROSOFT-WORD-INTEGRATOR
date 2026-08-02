class UserNotFoundException(Exception):
    """
    Raised when a user does not exist.
    """

    def __init__(self, identifier):
        self.identifier = identifier

        super().__init__(
            f"User {identifier} was not found."
        )