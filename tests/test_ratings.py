from tests.conftest import client


def test_get_rating():

    response = client.get(
        "/ratings/1"
    )

    assert response.status_code in [200, 404]


def test_invalid_rating():

    response = client.post(
        "/ratings/1?value=10"
    )

    assert response.status_code in [400, 401, 403]


def test_rating_without_auth():

    response = client.post(
        "/ratings/1?value=5"
    )

    assert response.status_code in [401, 403]