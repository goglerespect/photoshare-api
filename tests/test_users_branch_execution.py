from tests.conftest import client
from tests.conftest import get_auth_headers


def test_users_branches():

    headers = get_auth_headers()

    # me
    me = client.get(
        "/users/me",
        headers=headers
    )

    assert me.status_code == 200

    # search
    search = client.get(
        "/users/search/?query=test",
        headers=headers
    )

    assert search.status_code in [
        200,
        403
    ]

    # active
    active = client.get(
        "/users/filter/active",
        headers=headers
    )

    assert active.status_code in [
        200,
        403
    ]

    # banned
    banned = client.get(
        "/users/filter/banned",
        headers=headers
    )

    assert banned.status_code in [
        200,
        403
    ]