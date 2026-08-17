import requests
from app.ui.utils.config import API_BASE_URL
class APIClient:

    def __init__(self, base_url=API_BASE_URL, timeout=5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.auth_token = None

    def set_auth_token(self, token):
        self.auth_token = token

    def clear_auth_token(self):
        self.auth_token = None

    def _headers(self):
        headers = {
            "Content-Type": "application/json"
        }

        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        return headers

    def post(self, path, json_body):
        url = f"{self.base_url}{path}"

        return requests.post(
            url,
            json=json_body,
            headers=self._headers(),
            timeout=self.timeout,
        )

    def get(self, path, params=None):
        url = f"{self.base_url}{path}"

        return requests.get(
            url,
            params=params,
            headers=self._headers(),
            timeout=self.timeout,
        )

    def put(self, path, json_body=None):
        url = f"{self.base_url}{path}"

        return requests.put(
            url,
            json=json_body,
            headers=self._headers(),
            timeout=self.timeout,
        )

    def patch(self, path, json_body=None):
        url = f"{self.base_url}{path}"

        return requests.patch(
            url,
            json=json_body,
            headers=self._headers(),
            timeout=self.timeout,
        )

    def delete(self, path):
        url = f"{self.base_url}{path}"

        return requests.delete(
            url,
            headers=self._headers(),
            timeout=self.timeout,
        )


    def download(self, path):
        url = f"{self.base_url}{path}"

        return requests.get(
            url,
            headers={
                "Authorization": f"Bearer {self.auth_token}"
            } if self.auth_token else {},
            timeout=self.timeout,
        )

    def get_file(self, path, params=None):
        url = f"{self.base_url}{path}"

        return requests.get(
            url,
            params=params,
            headers=self._headers(),
            timeout=self.timeout,
        )

    def post_file(self, path, file_path):
        url = f"{self.base_url}{path}"

        with open(file_path, "rb") as file:
            return requests.post(
                url,
                files={
                    "file": (
                        file_path.split("\\")[-1],
                        file,
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
                },
                headers={
                    "Authorization": (
                        f"Bearer {self.auth_token}"
                        if self.auth_token
                        else ""
                    )
                },
                timeout=self.timeout,
            )


api_client = APIClient()


    