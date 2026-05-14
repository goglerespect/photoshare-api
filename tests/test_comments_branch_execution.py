from tests.conftest import client
from tests.conftest import get_auth_headers


def test_comment_branches():

    headers = get_auth_headers()

    # create comment
    create_response = client.post(
        "/comments/1",
        headers=headers,
        json={
            "text": "hello"
        }
    )

    if create_response.status_code == 404:
        return

    comment = create_response.json()

    comment_id = comment["id"]

    # get comments
    get_response = client.get(
        "/comments/photo/1"
    )

    assert get_response.status_code in [
        200,
        404
    ]

    # update
    update_response = client.put(
        f"/comments/{comment_id}",
        headers=headers,
        json={
            "text": "updated"
        }
    )

    assert update_response.status_code in [
        200,
        403
    ]

    # delete
    delete_response = client.delete(
        f"/comments/{comment_id}",
        headers=headers
    )

    assert delete_response.status_code in [
        200,
        403
    ]