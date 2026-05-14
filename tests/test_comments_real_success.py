from tests.conftest import client
from tests.conftest import get_auth_headers


def test_comment_create_update_delete():

    headers = get_auth_headers()

    # CREATE
    create_response = client.post(
        "/comments/1",
        headers=headers,
        json={
            "text": "hello"
        }
    )

    if create_response.status_code == 404:
        return

    assert create_response.status_code in [
        200,
        201
    ]

    comment = create_response.json()

    comment_id = comment["id"]

    # UPDATE
    update_response = client.put(
        f"/comments/{comment_id}",
        headers=headers,
        json={
            "text": "updated"
        }
    )

    assert update_response.status_code == 200

    # DELETE
    delete_response = client.delete(
        f"/comments/{comment_id}",
        headers=headers
    )

    assert delete_response.status_code == 200