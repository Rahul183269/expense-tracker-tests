import pytest



def test_create_expense(client):
    response = client.post(
        "/expenses",
        json={"title": "Lunch", "amount": 250.0, "category": "food"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Lunch"
    assert body["amount"] == 250.0


def test_get_expense_not_found(client):
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
def test_create_expense_invalid_input(client, payload):
    response = client.post("/expenses", json=payload)
    assert response.status_code == 422


def test_list_expenses_empty(client):
    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.json() == []


def test_list_expenses_after_create(client):
    client.post(
        "/expenses",
        json={"title": "Lunch", "amount": 250.0, "category": "food"},
    )
    client.post(
        "/expenses",
        json={"title": "Bus", "amount": 40.0, "category": "travel"},
    )
    response = client.get("/expenses")
    assert len(response.json()) == 2

def test_update_expense(client):
    client.post(
        "/expenses",
        json={"title": "Lunch", "amount": 250.0, "category": "food"},
    )
    response = client.put(
        "/expenses/1",
        json={"title": "Dinner", "amount": 400.0, "category": "food"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Dinner"
    assert response.json()["amount"] == 400.0


def test_update_expense_not_found(client):
    response = client.put(
        "/expenses/9999",
        json={"title": "Dinner", "amount": 400.0, "category": "food"},
    )
    assert response.status_code == 404


def test_delete_expense(client):
    client.post(
        "/expenses",
        json={"title": "Lunch", "amount": 250.0, "category": "food"},
    )
    response = client.delete("/expenses/1")
    assert response.status_code == 204
    assert client.get("/expenses/1").status_code == 404


def test_delete_expense_not_found(client):
    response = client.delete("/expenses/9999")
    assert response.status_code == 404