from tests.conftest import client
from tests.conftest import get_auth_headers


def test_make_moderator_not_found():

    headers = get_auth_headers()

    response = client.put(
        "/users/make-moderator/999999",
        headers=headers
    )

    # User not found
    assert response.status_code == 404


def test_remove_moderator_not_found():

    headers = get_auth_headers()

    response = client.put(
        "/users/remove-moderator/999999",
        headers=headers
    )

    # User not found
    assert response.status_code == 404


def test_ban_user_not_found():

    headers = get_auth_headers()

    response = client.put(
        "/users/ban/999999",
        headers=headers
    )

    # User not found
    assert response.status_code == 404