from tests.conftest import client
from tests.conftest import get_auth_headers


def test_create_photo_validation():

    headers = get_auth_headers()

    response = client.post(
        "/photos/",
        headers=headers,
        data={
            "title": "",
            "description": ""
        }
    )

    assert response.status_code in [400, 422]


def test_update_nonexistent_photo_real():

    headers = get_auth_headers()

    response = client.put(
        "/photos/999999",
        headers=headers,
        json={
            "title": "updated",
            "description": "updated"
        }
    )

    assert response.status_code == 404


def test_delete_nonexistent_photo_real():

    headers = get_auth_headers()

    response = client.delete(
        "/photos/999999",
        headers=headers
    )

    assert response.status_code == 404


def test_transform_nonexistent_photo_real():

    headers = get_auth_headers()

    response = client.post(
        "/photos/transform/999999",
        headers=headers
    )

    assert response.status_code == 404