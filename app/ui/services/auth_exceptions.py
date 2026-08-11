class AuthError(Exception):
    pass


class EmptyFieldError(AuthError):
    pass


class InvalidEmailFormatError(AuthError):
    pass


class InvalidCredentialsError(AuthError):
    pass


class EmailNotVerifiedError(AuthError):
    pass


class ServerUnavailableError(AuthError):
    pass


class NetworkError(AuthError):
    pass


class PasswordMismatchError(AuthError):
    pass


class WeakPasswordError(AuthError):
    pass


class EmailAlreadyRegisteredError(AuthError):
    pass


class InvalidTokenError(AuthError):
    pass


class ExpiredTokenError(AuthError):
    pass