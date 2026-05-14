from tests.conftest import (
    client,
    get_admin_headers
)


def test_comment_delete_success():

    headers = get_admin_headers()

    response = client.delete(
        "/comments/1",
        headers=headers
    )

    assert response.status_code in [
        200,
        404
    ]