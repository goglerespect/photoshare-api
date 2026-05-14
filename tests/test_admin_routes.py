from tests.conftest import client
from tests.conftest import get_auth_headers


def test_make_moderator_nonexistent_user():

    headers = get_auth_headers()

    response = client.put(
        "/users/make-moderator/999999",
        headers=headers
    )

    # User not found
    assert response.status_code == 404


def test_remove_moderator_nonexistent_user():

    headers = get_auth_headers()

    response = client.put(
        "/users/remove-moderator/999999",
        headers=headers
    )

    # User not found
    assert response.status_code == 404


def test_unban_nonexistent_user():

    headers = get_auth_headers()

    response = client.put(
        "/users/unban/999999",
        headers=headers
    )

    # User not found
    assert response.status_code == 404


def test_get_ratings_nonexistent_photo():

    headers = get_auth_headers()

    response = client.get(
        "/ratings/photo/999999",
        headers=headers
    )

    # Empty ratings list
    assert response.status_code == 200