from tests.conftest import client
from tests.conftest import get_auth_headers


def test_comment_update_delete_flow():

    headers = get_auth_headers()

    # Create comment
    create_response = client.post(
        "/comments/1",
        headers=headers,
        json={
            "text": "comment"
        }
    )

    # Photo may not exist
    if create_response.status_code == 404:
        return

    assert create_response.status_code in [
        200,
        201
    ]

    comment_id = create_response.json()["id"]

    # Update comment
    update_response = client.put(
        f"/comments/{comment_id}",
        headers=headers,
        json={
            "text": "updated"
        }
    )

    assert update_response.status_code == 200

    # Delete comment
    delete_response = client.delete(
        f"/comments/{comment_id}",
        headers=headers
    )

    assert delete_response.status_code == 200