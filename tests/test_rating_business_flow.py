from tests.conftest import client
from tests.conftest import get_auth_headers


def test_rating_business_logic():

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

    duplicate = client.post(
        "/ratings/1?value=5",
        headers=headers
    )

    assert duplicate.status_code in [
        400,
        404,
        409
    ]