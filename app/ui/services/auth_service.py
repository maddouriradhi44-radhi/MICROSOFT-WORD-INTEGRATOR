"""
Business logic layer for authentication.

The UI layer communicates only with AuthService.
It must not directly call requests or the API client.
"""
import re
import requests
import keyring

from app.ui.api.api_client import api_client
from app.ui.utils.config import KEYRING_SERVICE_NAME

from app.ui.services.auth_exceptions import (
    EmptyFieldError,
    InvalidEmailFormatError,
    InvalidCredentialsError,
    EmailNotVerifiedError,
    ServerUnavailableError,
    NetworkError,
    PasswordMismatchError,
    WeakPasswordError,
    EmailAlreadyRegisteredError,
    InvalidTokenError,
    ExpiredTokenError,
)

# ============================================================================
# Email validation
# ============================================================================

EMAIL_REGEX = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)


# ============================================================================
# Password validation
# ============================================================================

def password_requirements_status(password: str) -> dict:
    """
    Return the status of each password security requirement.

    Used by Register and Reset Password screens to display
    password requirements.
    """
    return {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digit": bool(re.search(r"\d", password)),
        "special": bool(re.search(r"[^A-Za-z0-9]", password)),
    }


# ============================================================================
# Authentication result
# ============================================================================

class AuthResult:
    """
    Represents a successful authentication.

    The JWT token comes from /auth/login.
    User information and role are retrieved from /auth/me.
    """

    def __init__(self, user, role, token):
        self.user = user
        self.role = role
        self.token = token


# ============================================================================
# Authentication service
# ============================================================================

class AuthService:
    """
    High-level authentication service used by the frontend.

    Responsibilities:
    - Validate authentication inputs
    - Communicate with authentication API
    - Translate HTTP/network errors into frontend exceptions
    - Store authentication token
    - Retrieve authenticated user information
    - Manage logout
    """

    # ------------------------------------------------------------------------
    # Login
    # ------------------------------------------------------------------------

    def login(self, email: str, password: str) -> AuthResult:
        """
        Authenticate a user.

        Flow:
            1. Validate local inputs
            2. POST /auth/login
            3. Check authentication result
            4. Store JWT
            5. GET /auth/me
            6. Retrieve user and role
            7. Store token securely
            8. Return AuthResult
        """

        # Step 1: local validation
        self._validate_inputs(email, password)

        # Step 2: login request
        try:
            response = api_client.post(
                "/auth/login",
                {
                    "email": email,
                    "password": password,
                },
            )

        except requests.exceptions.ConnectionError:
            raise NetworkError(
                "Impossible de contacter le serveur. "
                "Vérifiez votre connexion."
            )

        except requests.exceptions.Timeout:
            raise NetworkError(
                "Le serveur met trop de temps à répondre."
            )

        except requests.exceptions.RequestException:
            raise NetworkError(
                "Une erreur réseau est survenue."
            )

        # Step 3: interpret login response

        if response.status_code == 401:
            raise InvalidCredentialsError(
                "Email ou mot de passe incorrect."
            )

        if response.status_code == 403:
            raise EmailNotVerifiedError(
                "Votre adresse email n'est pas encore vérifiée."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Le serveur est actuellement indisponible."
            )

        if response.status_code not in (200, 201):
            raise ServerUnavailableError(
                f"Erreur inattendue du serveur "
                f"({response.status_code})."
            )

        # Step 4: extract JWT
        try:
            data = response.json()
        except ValueError:
            raise ServerUnavailableError(
                "La réponse du serveur est invalide."
            )

        token = (
            data.get("access_token")
            or data.get("token")
        )

        if not token:
            raise ServerUnavailableError(
                "Le serveur n'a pas retourné de token d'authentification."
            )

        # Step 5: store token in API client
        api_client.set_auth_token(token)

        # Step 6: retrieve authenticated user and role
        try:
            me_response = api_client.get("/auth/me")

        except requests.exceptions.ConnectionError:
            api_client.clear_auth_token()
            raise NetworkError(
                "Impossible de récupérer les informations utilisateur."
            )

        except requests.exceptions.Timeout:
            api_client.clear_auth_token()
            raise NetworkError(
                "Le serveur met trop de temps à répondre."
            )

        except requests.exceptions.RequestException:
            api_client.clear_auth_token()
            raise NetworkError(
                "Une erreur réseau est survenue."
            )

        # Handle /auth/me response
        if me_response.status_code == 401:
            api_client.clear_auth_token()
            raise InvalidCredentialsError(
                "La session d'authentification est invalide."
            )

        if me_response.status_code >= 500:
            api_client.clear_auth_token()
            raise ServerUnavailableError(
                "Le serveur est actuellement indisponible."
            )

        if me_response.status_code != 200:
            api_client.clear_auth_token()
            raise ServerUnavailableError(
                f"Impossible de récupérer le profil utilisateur "
                f"({me_response.status_code})."
            )

        try:
            user_data = me_response.json()
        except ValueError:
            api_client.clear_auth_token()
            raise ServerUnavailableError(
                "La réponse du serveur est invalide."
            )

        # Backend may return the role directly or inside user object.
        user = user_data.get("user", user_data)

        if isinstance(user_data, dict):
            role = user_data.get("role")

            if role is None and isinstance(user, dict):
                role = user.get("role")
        else:
            role = None

        # Step 7: create authentication result
        result = AuthResult(
            user=user,
            role=role,
            token=token,
        )

        # Step 8: persist JWT in OS keyring
        keyring.set_password(
            KEYRING_SERVICE_NAME,
            email,
            token,
        )

        return result

    # ------------------------------------------------------------------------
    # Register
    # ------------------------------------------------------------------------

    def register(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        confirm_password: str,
    ):
        """
        Register a new user.
        """

        required_fields = [
            (first_name, "First name is required."),
            (last_name, "Last name is required."),
            (email, "Email is required."),
            (password, "Password is required."),
            (confirm_password, "Please confirm your password."),
        ]

        for value, message in required_fields:
            if not value:
                raise EmptyFieldError(message)

        if not EMAIL_REGEX.match(email):
            raise InvalidEmailFormatError(
                "Please enter a valid email address."
            )

        if password != confirm_password:
            raise PasswordMismatchError(
                "Passwords do not match."
            )

        requirements = password_requirements_status(password)

        if not all(requirements.values()):
            raise WeakPasswordError(
                "Your password does not meet the security requirements."
            )

        try:
            response = api_client.post(
                "/auth/register",
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": password,
                },
            )

        except requests.exceptions.ConnectionError:
            raise NetworkError(
                "Unable to connect to the server."
            )

        except requests.exceptions.Timeout:
            raise NetworkError(
                "The server took too long to respond."
            )

        except requests.exceptions.RequestException:
            raise NetworkError(
                "A network error occurred."
            )

        if response.status_code == 409:
            raise EmailAlreadyRegisteredError(
                "This email address is already registered."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Something went wrong. Please try again."
            )

        if response.status_code not in (200, 201):
            raise ServerUnavailableError(
                f"Registration failed ({response.status_code})."
            )

        try:
            return response.json()
        except ValueError:
            return True

    # ------------------------------------------------------------------------
    # Email verification
    # ------------------------------------------------------------------------

    def verify_email(self, token: str):
        """
        Verify a user's email address.
        """

        if not token:
            raise InvalidTokenError(
                "The verification token is missing."
            )

        try:
            response = api_client.get(
                f"/auth/verify-email/{token}"
            )

        except requests.exceptions.ConnectionError:
            raise NetworkError(
                "Unable to connect to the server."
            )

        except requests.exceptions.Timeout:
            raise NetworkError(
                "The server took too long to respond."
            )

        except requests.exceptions.RequestException:
            raise NetworkError(
                "A network error occurred."
            )

        if response.status_code == 404:
            raise InvalidTokenError(
                "This verification link is invalid."
            )

        if response.status_code == 410:
            raise ExpiredTokenError(
                "This verification link has expired."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Something went wrong. Please try again."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Email verification failed ({response.status_code})."
            )

        try:
            return response.json()
        except ValueError:
            return True

    # ------------------------------------------------------------------------
    # Forgot password
    # ------------------------------------------------------------------------

    def forgot_password(self, email: str):
        """
        Request a password reset email.
        """

        if not email:
            raise EmptyFieldError(
                "Please enter your email address."
            )

        if not EMAIL_REGEX.match(email):
            raise InvalidEmailFormatError(
                "Please enter a valid email address."
            )

        try:
            response = api_client.post(
                "/auth/forgot-password",
                {
                    "email": email,
                },
            )

        except requests.exceptions.ConnectionError:
            raise NetworkError(
                "Unable to contact the server. Please try again."
            )

        except requests.exceptions.Timeout:
            raise NetworkError(
                "The server took too long to respond."
            )

        except requests.exceptions.RequestException:
            raise NetworkError(
                "A network error occurred."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Unable to contact the server. Please try again."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Password reset request failed "
                f"({response.status_code})."
            )

        try:
            return response.json()
        except ValueError:
            return True

    # ------------------------------------------------------------------------
    # Check reset token
    # ------------------------------------------------------------------------

    def check_reset_token(self, token: str):
        """
        Check whether a password reset token is valid.
        """

        if not token:
            raise InvalidTokenError(
                "The password reset token is missing."
            )

        try:
            response = api_client.get(
                f"/auth/reset-password/{token}"
            )

        except requests.exceptions.ConnectionError:
            raise NetworkError(
                "Unable to connect to the server."
            )

        except requests.exceptions.Timeout:
            raise NetworkError(
                "The server took too long to respond."
            )

        except requests.exceptions.RequestException:
            raise NetworkError(
                "A network error occurred."
            )

        if response.status_code == 404:
            raise InvalidTokenError(
                "This password reset link is invalid "
                "or no longer available."
            )

        if response.status_code == 410:
            raise ExpiredTokenError(
                "This password reset link has expired. "
                "Please request a new one."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Something went wrong. Please try again."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to validate reset token "
                f"({response.status_code})."
            )

        return True

    # ------------------------------------------------------------------------
    # Reset password
    # ------------------------------------------------------------------------

    def reset_password(
        self,
        token: str,
        new_password: str,
        confirm_password: str,
    ):
        """
        Reset the user's password.
        """

        if not token:
            raise InvalidTokenError(
                "The password reset token is missing."
            )

        if not new_password or not confirm_password:
            raise EmptyFieldError(
                "Please fill in both password fields."
            )

        if new_password != confirm_password:
            raise PasswordMismatchError(
                "Passwords do not match."
            )

        requirements = password_requirements_status(
            new_password
        )

        if not all(requirements.values()):
            raise WeakPasswordError(
                "Your password does not meet the security requirements."
            )

        try:
            response = api_client.post(
                "/auth/reset-password",
                {
                    "token": token,
                    "new_password": new_password,
                },
            )

        except requests.exceptions.ConnectionError:
            raise NetworkError(
                "Unable to connect to the server."
            )

        except requests.exceptions.Timeout:
            raise NetworkError(
                "The server took too long to respond."
            )

        except requests.exceptions.RequestException:
            raise NetworkError(
                "A network error occurred."
            )

        if response.status_code == 404:
            raise InvalidTokenError(
                "This password reset link is invalid "
                "or no longer available."
            )

        if response.status_code == 410:
            raise ExpiredTokenError(
                "This password reset link has expired."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Something went wrong. Please try again."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Password reset failed ({response.status_code})."
            )

        try:
            return response.json()
        except ValueError:
            return True

    # ------------------------------------------------------------------------
    # Logout
    # ------------------------------------------------------------------------

    def logout(self, email: str):
        """
        Clear the current authentication session.
        """

        api_client.clear_auth_token()

        try:
            keyring.delete_password(
                KEYRING_SERVICE_NAME,
                email,
            )
        except keyring.errors.PasswordDeleteError:
            pass

    # ------------------------------------------------------------------------
    # Local login validation
    # ------------------------------------------------------------------------

    def _validate_inputs(
        self,
        email: str,
        password: str,
    ):
        """
        Validate login fields before contacting the backend.
        """

        if not email:
            raise EmptyFieldError(
                "L'adresse email est requise."
            )

        if not password:
            raise EmptyFieldError(
                "Le mot de passe est requis."
            )

        if not EMAIL_REGEX.match(email):
            raise InvalidEmailFormatError(
                "Le format de l'email est invalide."
            )


# ============================================================================
# Shared service instance
# ============================================================================

auth_service = AuthService()