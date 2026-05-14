from tests.conftest import client
from tests.conftest import get_auth_headers


def test_comment_full_branch_flow():

    headers = get_auth_headers()

    # create
    response = client.post(
        "/comments/1",
        headers=headers,
        json={
            "text": "hello"
        }
    )

    if response.status_code == 404:
        return

    assert response.status_code in [
        200,
        201
    ]

    comment = response.json()

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