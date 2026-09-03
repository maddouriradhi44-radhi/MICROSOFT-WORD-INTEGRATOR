import requests

from api.api_client import api_client
from models.section import Section
from services.auth_exceptions import (
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

    def export_section(self, section_id):
        try:
            response = api_client.get(
                f"/sections/{section_id}/export"
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
                "You are not allowed to export this section."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Unable to export the section."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to export the section ({response.status_code})."
            )

        return response

    def import_section(self, section_id, file_path):
        try:
            response = api_client.post_file(
                f"/sections/{section_id}/import",
                file_path,
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
                "You are not allowed to import this section."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Unable to import the section."
            )

        if response.status_code != 200:
            try:
                detail = response.json().get(
                    "detail",
                    "Unable to import the section."
                )
            except ValueError:
                detail = (
                    f"Unable to import the section "
                    f"({response.status_code})."
                )

            raise ServerUnavailableError(detail)

        try:
            return response.json()

        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid response."
            )

    def get_ai_proposals(self, document_id: int):
        try:
            response = api_client.get(
                f"/ai/documents/{document_id}/proposals"
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
                "Unable to load AI proposals."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to load AI proposals ({response.status_code})."
            )

        try:
            data = response.json()

        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid AI proposals response."
            )

        if not isinstance(data, list):
            raise ServerUnavailableError(
                "The server returned an invalid AI proposals list."
            )

        return data


    def accept_ai_proposal(self, proposal_id, assigned_user_id=None):
        params = ""

        if assigned_user_id is not None:
            params = f"?assigned_user_id={assigned_user_id}"

        try:
            response = api_client.post(
                f"/ai/proposals/{proposal_id}/accept{params}",
                {},
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
                "You are not allowed to accept this proposal."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Unable to accept AI proposal."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to accept AI proposal "
                f"({response.status_code})."
            )

        try:
            return response.json()

        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid response."
            )


    def reject_ai_proposal(self, proposal_id, review_comment=None):

        try:
            response = api_client.post(
                f"/ai/proposals/{proposal_id}/reject",
                {
                    "review_comment": review_comment,
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
                "You are not allowed to reject this proposal."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Unable to reject AI proposal."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to reject AI proposal "
                f"({response.status_code})."
            )

        try:
            return response.json()

        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid response."
            )


section_service = SectionService()