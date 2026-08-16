import requests
from app.ui.api.api_client import api_client
from app.ui.services.auth_exceptions import (
    ServerUnavailableError,
    NetworkError,
)

class ProjectService:

    def get_projects(self):
        try:
            response = api_client.get("/projects")

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
                "Unable to load your projects."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to load your projects ({response.status_code})."
            )

        try:
            data = response.json()
        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid response."
            )

        if not isinstance(data, list):
            raise ServerUnavailableError(
                "The server returned an invalid projects list."
            )

        return data


project_service = ProjectService()