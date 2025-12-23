from fastapi import status
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_return_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}
