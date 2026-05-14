from tests.conftest import client
from tests.conftest import get_auth_headers


def test_update_profile_success():

    headers = get_auth_headers()

    response = client.put(
        "/users/me",
        headers=headers,
        json={
            "bio": "updated bio",
            "username": "updated_user"
        }
    )

    assert response.status_code == 200