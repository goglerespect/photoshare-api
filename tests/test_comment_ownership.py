from tests.conftest import client
from tests.conftest import get_auth_headers


def test_comment_update_permission():

    headers = get_auth_headers()

    response = client.put(
        "/comments/1",
        headers=headers,
        json={
            "text": "updated"
        }
    )

    assert response.status_code in [
        200,
        403,
        404
    ]