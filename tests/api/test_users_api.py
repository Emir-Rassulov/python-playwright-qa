import pytest
import requests

from test_data.api_config import BASE_URL


def test_get_user():
    response = requests.get(f"{BASE_URL}/users/1")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == 1
    assert body["firstName"] == "Emily"
    assert body["lastName"] == "Johnson"


@pytest.mark.parametrize(
    "user_id, expected_status",
    [
        (9999, 404),
        (0, 404),
        (-1, 404),
        ("abc", 400),
    ],
)
def test_get_invalid_user_id_returns_expected_status(user_id, expected_status):
    response = requests.get(f"{BASE_URL}/users/{user_id}")

    assert response.status_code == expected_status


def test_create_user():
    response = requests.post(
        f"{BASE_URL}/users/add",
        json={
            "firstName": "John",
            "lastName": "Doe",
            "age": 30,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["firstName"] == "John"
    assert body["lastName"] == "Doe"
    assert body["age"] == 30

    assert "id" in body
    assert isinstance(body["id"], int)


def test_update_user():
    response = requests.put(
        f"{BASE_URL}/users/1",
        json={
            "firstName": "John",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == 1
    assert body["firstName"] == "John"

def test_delete_user():
    response = requests.delete(f"{BASE_URL}/users/1")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == 1
    assert body["firstName"] == "Emily"
    assert body["lastName"] == "Johnson"
    assert body["isDeleted"] is True
    assert "deletedOn" in body