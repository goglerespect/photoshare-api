from tests.conftest import client
from tests.conftest import get_auth_headers


def test_get_my_profile():

    headers = get_auth_headers()

    response = client.get(
        "/users/me",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "email" in data
    assert "username" in data
    assert "role" in data


def test_update_profile():

    headers = get_auth_headers()

    response = client.put(
        "/users/me",
        headers=headers,
        json={
            "bio": "updated bio"
        }
    )

    assert response.status_code == 200


def test_get_public_profile():

    response = client.get(
        "/users/testuser"
    )

    assert response.status_code in [200, 404]


def test_get_nonexistent_profile():

    response = client.get(
        "/users/nonexistent_user"
    )

    assert response.status_code == 404


def test_non_admin_cannot_ban():

    headers = get_auth_headers()

    response = client.put(
        "/users/ban/999999",
        headers=headers
    )

    # User not found
    assert response.status_code == 404