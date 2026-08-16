import requests

from app.ui.api.api_client import api_client
from app.ui.models.section import Section
from app.ui.services.auth_exceptions import (
    ServerUnavailableError,
    NetworkError,
)


class SectionService:

    def get_my_sections(self):
        try:
            response = api_client.get("/sections/my-sections")

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
                "Unable to load your sections."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to load your sections ({response.status_code})."
            )

        try:
            data = response.json()

        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid response."
            )

        if not isinstance(data, list):
            raise ServerUnavailableError(
                "The server returned an invalid sections list."
            )

        return [
            Section.from_dict(item)
            for item in data
        ]

    def update_section(self, section_id, content):
        try:
            response = api_client.patch(
                f"/sections/{section_id}",
                {
                    "content": content,
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

        if response.status_code == 401:
            raise NetworkError(
                "Your authentication session has expired."
            )

        if response.status_code == 403:
            raise NetworkError(
                "You are not allowed to modify this section."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Unable to update the section."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to update the section ({response.status_code})."
            )

        try:
            data = response.json()

        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid response."
            )

        return Section.from_dict(data)


section_service = SectionService()