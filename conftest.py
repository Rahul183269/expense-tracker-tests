import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    client = TestClient(app)
    client.delete("/reset")
    return client