from tests.conftest import client


def test_get_comments():

    response = client.get(
        "/comments/photo/1"
    )

    assert response.status_code in [200, 404]


def test_create_comment_without_auth():

    response = client.post(
        "/comments/1",
        json={
            "text": "test"
        }
    )

    assert response.status_code in [401, 403]


def test_delete_comment_without_auth():

    response = client.delete(
        "/comments/1"
    )

    assert response.status_code in [401, 403]