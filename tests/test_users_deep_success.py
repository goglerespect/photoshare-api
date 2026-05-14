from tests.conftest import client
from tests.conftest import get_auth_headers


def test_users_search_flow():

    headers = get_auth_headers()

    response = client.get(
        "/users/search/?query=test",
        headers=headers
    )

    assert response.status_code in [
        200,
        403
    ]


def test_filter_active_flow():

    headers = get_auth_headers()

    response = client.get(
        "/users/filter/active",
        headers=headers
    )

    assert response.status_code in [
        200,
        403
    ]


def test_filter_banned_flow():

    headers = get_auth_headers()

    response = client.get(
        "/users/filter/banned",
        headers=headers
    )

    assert response.status_code in [
        200,
        403
    ]