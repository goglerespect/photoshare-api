from tests.conftest import client
from tests.conftest import get_auth_headers


def test_get_me_success():

    headers = get_auth_headers()

    response = client.get(
        "/users/me",
        headers=headers
    )

    assert response.status_code == 200


def test_update_profile_success():

    headers = get_auth_headers()

    response = client.put(
        "/users/me",
        headers=headers,
        json={
            "bio": "new bio"
        }
    )

    assert response.status_code == 200


def test_search_users_success():

    headers = get_auth_headers()

    response = client.get(
        "/users/search/?query=user",
        headers=headers
    )

    assert response.status_code in [200, 403]


def test_filter_active_users():

    headers = get_auth_headers()

    response = client.get(
        "/users/filter/active",
        headers=headers
    )

    assert response.status_code in [200, 403]


def test_filter_banned_users():

    headers = get_auth_headers()

    response = client.get(
        "/users/filter/banned",
        headers=headers
    )

    assert response.status_code in [200, 403]