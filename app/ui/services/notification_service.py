import requests
from api.api_client import api_client
from services.auth_exceptions import (
    ServerUnavailableError,
    NetworkError,
)
class NotificationService:

    def get_notifications(self, page: int = 1, page_size: int = 5):
        try:
            response = api_client.get(
                "/notifications",
                params={
                    "page": page,
                    "page_size": page_size,
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

        if response.status_code >= 500:
            raise ServerUnavailableError(
                "Unable to load notifications."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to load notifications "
                f"({response.status_code})."
            )

        try:
            data = response.json()
        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid response."
            )

        if not isinstance(data, dict):
            raise ServerUnavailableError(
                "The server returned an invalid notifications response."
            )

        if "items" not in data:
            raise ServerUnavailableError(
                "The server response does not contain notifications."
            )

        return data
  
    def get_unread_count(self):
        try:
            response = api_client.get("/notifications/unread/count")

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
                "Unable to load unread notifications count."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to load unread notifications count "
                f"({response.status_code})."
            )

        try:
            data = response.json()
        except ValueError:
            raise ServerUnavailableError(
                "The server returned an invalid unread count."
            )

        if isinstance(data, int):
            return data

        if isinstance(data, dict) and "count" in data:
            return int(data["count"])

        raise ServerUnavailableError(
            "The server returned an invalid unread count."
        )





    def mark_as_read(self, notification_id: int):
        try:
            response = api_client.patch(
                f"/notifications/{notification_id}/read"
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
                "Unable to mark notification as read."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to mark notification as read "
                f"({response.status_code})."
            )

        return response

    def mark_all_as_read(self):
        try:
            response = api_client.patch(
                "/notifications/read-all"
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
                "Unable to mark notifications as read."
            )

        if response.status_code != 200:
            raise ServerUnavailableError(
                f"Unable to mark notifications as read "
                f"({response.status_code})."
            )

        return response
notification_service = NotificationService()