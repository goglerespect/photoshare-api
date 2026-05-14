from tests.conftest import client
from tests.conftest import get_auth_headers


def test_edit_comment_without_auth():

    response = client.put(
        "/comments/1",
        json={
            "text": "updated"
        }
    )

    assert response.status_code in [401, 403]


def test_delete_comment_nonexistent():

    headers = get_auth_headers()

    response = client.delete(
        "/comments/999999",
        headers=headers
    )

    assert response.status_code in [403, 404]


def test_create_comment_nonexistent_photo():

    headers = get_auth_headers()

    response = client.post(
        "/comments/999999",
        headers=headers,
        json={
            "text": "test"
        }
    )

    assert response.status_code == 404