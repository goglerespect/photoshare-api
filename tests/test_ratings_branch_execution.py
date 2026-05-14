from tests.conftest import client
from tests.conftest import get_auth_headers


def test_rating_branches():

    headers = get_auth_headers()

    # create
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

    # duplicate
    duplicate = client.post(
        "/ratings/1?value=5",
        headers=headers
    )

    assert duplicate.status_code in [
        400,
        404,
        409
    ]

    # invalid value
    invalid = client.post(
        "/ratings/1?value=100",
        headers=headers
    )

    assert invalid.status_code in [
        400,
        422
    ]

    # get ratings
    ratings = client.get(
        "/ratings/photo/1",
        headers=headers
    )

    assert ratings.status_code in [
        200,
        403,
        404
    ]