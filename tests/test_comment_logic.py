from tests.conftest import client
from tests.conftest import get_auth_headers


def test_comment_not_found():

    headers = get_auth_headers()

    response = client.put(
        "/comments/999999",
        headers=headers,
        json={
            "text": "updated"
        }
    )

    assert response.status_code == 404


def test_delete_comment_not_found():

    headers = get_auth_headers()

    response = client.delete(
        "/comments/999999",
        headers=headers
    )

    assert response.status_code == 404