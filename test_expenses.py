import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_expense():
    response = client.post(
        "/expenses",
        json={"title": "Lunch", "amount": 250.0, "category": "food"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Lunch"
    assert body["amount"] == 250.0


def test_get_expense_not_found():
    response = client.get("/expenses/9999")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "", "amount": 100.0, "category": "food"},
        {"title": "Lunch", "amount": -500.0, "category": "food"},
        {"title": "Lunch", "amount": 0, "category": "food"},
        {"title": "Lunch", "amount": 100.0, "category": ""},
        {"title": "Lunch", "amount": 100.0, "category": 123},
        {"amount": 100.0, "category": "food"},
        {"title": "Lunch", "category": "food"},
        {"title": "Lunch", "amount": "abc", "category": "food"},
    ],
)
def test_create_expense_invalid_input(payload):
    response = client.post("/expenses", json=payload)
    assert response.status_code == 422