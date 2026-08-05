"""
Basic application tests.
"""


def test_application_running(client):
    """
    Check that API is reachable.
    """

    response = client.get("/docs")

    assert response.status_code == 200