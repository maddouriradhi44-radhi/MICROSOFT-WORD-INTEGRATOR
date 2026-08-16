import requests

from app.ui.api.api_client import api_client
from app.ui.services.auth_exceptions import (
    ServerUnavailableError,
    NetworkError,
)


class VersionService:

    def get_current_version(self, section_id):
        try:
            response = api_client.get(
                f"/versions/current/{section_id}"
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

        if response.status_code == 401:
            raise NetworkError(
                "Your authentication session has expired."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Unable to load the current section version."
            )

        if response.status_code == 404:
            return None

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to load the current section version "
                f"({response.status_code})."
            )

        try:
            return response.json()

        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid version response."
            )


version_service = VersionService()