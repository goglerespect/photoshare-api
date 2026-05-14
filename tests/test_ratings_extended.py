from tests.conftest import client
from tests.conftest import get_auth_headers


def test_rate_nonexistent_photo():

    headers = get_auth_headers()

    response = client.post(
        "/ratings/999999?value=5",
        headers=headers
    )

    assert response.status_code == 404


def test_invalid_low_rating():

    headers = get_auth_headers()

    response = client.post(
        "/ratings/1?value=0",
        headers=headers
    )

    assert response.status_code == 400


def test_invalid_high_rating():

    headers = get_auth_headers()

    response = client.post(
        "/ratings/1?value=10",
        headers=headers
    )

    assert response.status_code == 400


def test_delete_nonexistent_rating():

    headers = get_auth_headers()

    response = client.delete(
        "/ratings/999999",
        headers=headers
    )

    assert response.status_code in [403, 404]