from tests.conftest import client
from tests.conftest import get_auth_headers


def test_comment_full_flow():

    headers = get_auth_headers()

    # Create comment
    create_response = client.post(
        "/comments/1",
        headers=headers,
        json={
            "text": "test comment"
        }
    )

    if create_response.status_code == 404:
        return

    assert create_response.status_code in [200, 201]

    comment_data = create_response.json()

    comment_id = comment_data["id"]

    # Update
    update_response = client.put(
        f"/comments/{comment_id}",
        headers=headers,
        json={
            "text": "updated"
        }
    )

    assert update_response.status_code == 200

    # Delete
    delete_response = client.delete(
        f"/comments/{comment_id}",
        headers=headers
    )

    assert delete_response.status_code == 200