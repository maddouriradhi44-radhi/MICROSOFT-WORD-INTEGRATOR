import os

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://localhost:8000"
)

KEYRING_SERVICE_NAME = "doc_platform"