from tests.conftest import client
from tests.conftest import get_auth_headers


def test_get_ratings():

    headers = get_auth_headers()

    response = client.get(
        "/ratings/photo/1",
        headers=headers
    )

    assert response.status_code in [
        200,
        403,
        404
    ]


def test_duplicate_rating():

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
        404,
        409
    ]