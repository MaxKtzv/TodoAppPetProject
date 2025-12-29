from fastapi import status
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_return_healthcheck() -> None:
    """Test the health check endpoint for operational status.

    Returns:
        None.

    Raises:
        AssertionError: If the response status code is not 200 or the
            response body does not match the expected value.
    """
    response = client.get("/healthcheck")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}
