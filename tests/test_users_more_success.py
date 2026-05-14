from tests.conftest import client
from tests.conftest import get_auth_headers


def test_update_profile():

    headers = get_auth_headers()

    response = client.put(
        "/users/me",
        headers=headers,
        json={
            "bio": "new bio",
            "username": "new_username"
        }
    )

    assert response.status_code == 200


def test_get_profile():

    headers = get_auth_headers()

    response = client.get(
        "/users/me",
        headers=headers
    )

    assert response.status_code == 200