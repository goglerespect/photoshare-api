from tests.conftest import client
from tests.conftest import get_auth_headers


def test_invalid_rating_zero():

    headers = get_auth_headers()

    response = client.post(
        "/ratings/1?value=0",
        headers=headers
    )

    assert response.status_code == 400


def test_invalid_rating_six():

    headers = get_auth_headers()

    response = client.post(
        "/ratings/1?value=6",
        headers=headers
    )

    assert response.status_code == 400


def test_rating_nonexistent_photo():

    headers = get_auth_headers()

    response = client.post(
        "/ratings/999999?value=5",
        headers=headers
    )

    assert response.status_code == 404