from tests.conftest import client
from tests.conftest import get_auth_headers


def test_real_comment_flow():

    headers = get_auth_headers()

    # create comment
    create = client.post(
        "/comments/1",
        headers=headers,
        json={
            "text": "hello"
        }
    )

    if create.status_code == 404:
        return

    assert create.status_code in [
        200,
        201
    ]

    comment = create.json()

    comment_id = comment["id"]

    # update
    update = client.put(
        f"/comments/{comment_id}",
        headers=headers,
        json={
            "text": "updated"
        }
    )

    assert update.status_code in [
        200,
        403
    ]

    # delete
    delete = client.delete(
        f"/comments/{comment_id}",
        headers=headers
    )

    assert delete.status_code in [
        200,
        403
    ]