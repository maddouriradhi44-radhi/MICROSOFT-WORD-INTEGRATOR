import requests

from api.api_client import api_client
from models.version import Version
from services.auth_exceptions import (
    ServerUnavailableError,
    NetworkError,
)


class VersionService:

    # ==========================================================
    # CURRENT VERSION
    # ==========================================================

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

        if response.status_code == 404:
            return None

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Unable to load the current section version."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to load the current section version "
                f"({response.status_code})."
            )

        try:
            data = response.json()

        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid version response."
            )

        return Version.from_dict(data)

    # ==========================================================
    # VERSION HISTORY
    # ==========================================================

    def get_history(self, section_id):
        try:
            response = api_client.get(
                f"/versions/section/{section_id}"
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
                "You are not allowed to access this version history."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Unable to load version history."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to load version history "
                f"({response.status_code})."
            )

        try:
            data = response.json()

        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid version history."
            )

        # Backend response:
        #
        # {
        #     "versions": [...]
        # }

        versions_data = data.get("versions", [])

        if not isinstance(versions_data, list):
            raise ServerUnavailableError(
                "The server returned an invalid versions list."
            )

        return [
            Version.from_dict(item)
            for item in versions_data
        ]

    # ==========================================================
    # ARCHIVED VERSIONS
    # ==========================================================

    def get_archived_versions(self, section_id):
        try:
            response = api_client.get(
                f"/versions/archived/{section_id}"
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
                "You are not allowed to access archived versions."
            )

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Unable to load archived versions."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to load archived versions "
                f"({response.status_code})."
            )

        try:
            data = response.json()

        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid archived versions response."
            )

        versions_data = data.get("versions", [])

        if not isinstance(versions_data, list):
            raise ServerUnavailableError(
                "The server returned an invalid versions list."
            )

        return [
            Version.from_dict(item)
            for item in versions_data
        ]

    # ==========================================================
    # RESTORE VERSION
    # ==========================================================

    def restore_version(self, version_id):
        try:
            response = api_client.post(
                "/versions/restore",
                {
                    "version_id": version_id,
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
                "You are not allowed to restore this version."
            )

        if response.status_code == 404:
            return None

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Unable to restore the selected version."
            )

        if response.status_code != 200:
            try:
                detail = response.json().get(
                    "detail",
                    "Unable to restore the selected version."
                )
            except ValueError:
                detail = (
                    f"Unable to restore the selected version "
                    f"({response.status_code})."
                )

            raise ServerUnavailableError(detail)

        try:
            data = response.json()

        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid restored version."
            )

        return Version.from_dict(data)


version_service = VersionService()