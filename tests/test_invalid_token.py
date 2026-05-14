from tests.conftest import client


def test_invalid_token():

    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid"
        }
    )

    assert response.status_code in [
        401,
        403
    ]