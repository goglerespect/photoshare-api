from tests.conftest import client
from tests.conftest import get_auth_headers


def test_update_photo_without_auth():

    response = client.put(
        "/photos/1",
        json={
            "title": "updated",
            "description": "updated"
        }
    )

    assert response.status_code in [401, 403]


def test_delete_photo_without_auth():

    response = client.delete(
        "/photos/1"
    )

    assert response.status_code in [401, 403]


def test_transform_photo_without_auth():

    response = client.post(
        "/photos/transform/1"
    )

    assert response.status_code in [401, 403]


def test_create_rating_without_auth():

    response = client.post(
        "/ratings/1?value=5"
    )

    assert response.status_code in [401, 403]


def test_delete_rating_without_auth():

    response = client.delete(
        "/ratings/1"
    )

    assert response.status_code in [401, 403]


def test_make_moderator_without_auth():

    response = client.put(
        "/users/make-moderator/1"
    )

    assert response.status_code in [401, 403]