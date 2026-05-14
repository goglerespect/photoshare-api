from tests.conftest import client
from tests.conftest import get_auth_headers


def test_full_user_flow():

    headers = get_auth_headers()

    # Get profile
    response = client.get(
        "/users/me",
        headers=headers
    )

    assert response.status_code == 200

    # Update profile
    response = client.put(
        "/users/me",
        headers=headers,
        json={
            "bio": "new bio"
        }
    )

    assert response.status_code == 200