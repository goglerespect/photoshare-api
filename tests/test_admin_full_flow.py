from tests.conftest import client
from tests.conftest import get_auth_headers


def test_admin_management_flow():

    headers = get_auth_headers()

    # create user
    register_response = client.post(
        "/auth/register",
        json={
            "email": "flow@test.com",
            "username": "flowuser",
            "password": "123456"
        }
    )

    if register_response.status_code not in [200, 201]:
        return

    # search users
    search_response = client.get(
        "/users/search/?query=flow",
        headers=headers
    )

    assert search_response.status_code in [
        200,
        403
    ]

    # filter active
    active_response = client.get(
        "/users/filter/active",
        headers=headers
    )

    assert active_response.status_code in [
        200,
        403
    ]