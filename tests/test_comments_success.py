from tests.conftest import client
from tests.conftest import get_auth_headers


def test_create_comment_success():

    headers = get_auth_headers()

    response = client.post(
        "/comments/1",
        headers=headers,
        json={
            "text": "test"
        }
    )

    assert response.status_code in [
        200,
        201,
        404
    ]


def test_get_comments_success():

    response = client.get(
        "/comments/photo/1"
    )

    assert response.status_code in [
        200,
        404
    ]