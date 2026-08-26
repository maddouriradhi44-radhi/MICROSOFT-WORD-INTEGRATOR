import time
import requests

from utils.config import API_BASE_URL


class APIClient:

    def __init__(self, base_url=API_BASE_URL, timeout=5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.auth_token = None

    # ==========================================================
    # AUTH TOKEN
    # ==========================================================

    def set_auth_token(self, token):
        self.auth_token = token

    def clear_auth_token(self):
        self.auth_token = None

    # ==========================================================
    # HEADERS
    # ==========================================================

    def _headers(self):
        headers = {
            "Content-Type": "application/json"
        }

        if self.auth_token:
            headers["Authorization"] = (
                f"Bearer {self.auth_token}"
            )

        return headers

    # ==========================================================
    # POST
    # ==========================================================

    def post(self, path, json_body):
        url = f"{self.base_url}{path}"

        start = time.perf_counter()

        try:
            response = requests.post(
                url,
                json=json_body,
                headers=self._headers(),
                timeout=self.timeout,
            )

            return response

        finally:
            elapsed = time.perf_counter() - start

            print(
                f"[API POST] {path} "
                f"-> {response.status_code if 'response' in locals() else 'ERROR'} "
                f"({elapsed:.3f}s)"
            )

    # ==========================================================
    # GET
    # ==========================================================

    def get(self, path, params=None):
        url = f"{self.base_url}{path}"

        start = time.perf_counter()

        try:
            response = requests.get(
                url,
                params=params,
                headers=self._headers(),
                timeout=self.timeout,
            )

            return response

        finally:
            elapsed = time.perf_counter() - start

            print(
                f"[API GET] {path} "
                f"-> {response.status_code if 'response' in locals() else 'ERROR'} "
                f"({elapsed:.3f}s)"
            )

    # ==========================================================
    # PUT
    # ==========================================================

    def put(self, path, json_body=None):
        url = f"{self.base_url}{path}"

        start = time.perf_counter()

        try:
            response = requests.put(
                url,
                json=json_body,
                headers=self._headers(),
                timeout=self.timeout,
            )

            return response

        finally:
            elapsed = time.perf_counter() - start

            print(
                f"[API PUT] {path} "
                f"-> {response.status_code if 'response' in locals() else 'ERROR'} "
                f"({elapsed:.3f}s)"
            )

    # ==========================================================
    # PATCH
    # ==========================================================

    def patch(self, path, json_body=None):
        url = f"{self.base_url}{path}"

        start = time.perf_counter()

        try:
            response = requests.patch(
                url,
                json=json_body,
                headers=self._headers(),
                timeout=self.timeout,
            )

            return response

        finally:
            elapsed = time.perf_counter() - start

            print(
                f"[API PATCH] {path} "
                f"-> {response.status_code if 'response' in locals() else 'ERROR'} "
                f"({elapsed:.3f}s)"
            )

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(self, path):
        url = f"{self.base_url}{path}"

        start = time.perf_counter()

        try:
            response = requests.delete(
                url,
                headers=self._headers(),
                timeout=self.timeout,
            )

            return response

        finally:
            elapsed = time.perf_counter() - start

            print(
                f"[API DELETE] {path} "
                f"-> {response.status_code if 'response' in locals() else 'ERROR'} "
                f"({elapsed:.3f}s)"
            )

    # ==========================================================
    # DOWNLOAD
    # ==========================================================

    def download(self, path):
        url = f"{self.base_url}{path}"

        start = time.perf_counter()

        try:
            response = requests.get(
                url,
                headers={
                    "Authorization": (
                        f"Bearer {self.auth_token}"
                    )
                    if self.auth_token
                    else {}
                },
                timeout=self.timeout,
            )

            return response

        finally:
            elapsed = time.perf_counter() - start

            print(
                f"[API DOWNLOAD] {path} "
                f"-> {response.status_code if 'response' in locals() else 'ERROR'} "
                f"({elapsed:.3f}s)"
            )

    # ==========================================================
    # GET FILE
    # ==========================================================

    def get_file(self, path, params=None):
        url = f"{self.base_url}{path}"

        start = time.perf_counter()

        try:
            response = requests.get(
                url,
                params=params,
                headers=self._headers(),
                timeout=self.timeout,
            )

            return response

        finally:
            elapsed = time.perf_counter() - start

            print(
                f"[API GET FILE] {path} "
                f"-> {response.status_code if 'response' in locals() else 'ERROR'} "
                f"({elapsed:.3f}s)"
            )

    # ==========================================================
    # POST FILE
    # ==========================================================

    def post_file(self, path, file_path, data=None):
        url = f"{self.base_url}{path}"

        start = time.perf_counter()

        try:
            with open(file_path, "rb") as file:

                response = requests.post(
                    url,
                    files={
                        "file": (
                            file_path.split("\\")[-1],
                            file,
                            (
                                "application/"
                                "vnd.openxmlformats-officedocument."
                                "wordprocessingml.document"
                            ),
                        )
                    },
                    data=data or {},
                    headers={
                        "Authorization": (
                            f"Bearer {self.auth_token}"
                            if self.auth_token
                            else ""
                        )
                    },
                    timeout=self.timeout,
                )

                return response

        finally:
            elapsed = time.perf_counter() - start

            print(
                f"[API POST FILE] {path} "
                f"-> {response.status_code if 'response' in locals() else 'ERROR'} "
                f"({elapsed:.3f}s)"
            )
api_client = APIClient()