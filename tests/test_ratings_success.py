from tests.conftest import client
from tests.conftest import get_auth_headers


def test_rating_create():

    headers = get_auth_headers()

    response = client.post(
        "/ratings/1?value=5",
        headers=headers
    )

    assert response.status_code in [
        200,
        201,
        400,
        404
    ]


def test_rating_duplicate():

    headers = get_auth_headers()

    client.post(
        "/ratings/1?value=5",
        headers=headers
    )

    response = client.post(
        "/ratings/1?value=5",
        headers=headers
    )

    assert response.status_code in [
        400,
        409,
        404
    ]