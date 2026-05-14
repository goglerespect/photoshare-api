from tests.conftest import client
from tests.conftest import get_auth_headers


def get_token():

    headers = get_auth_headers()

    return headers["Authorization"].split(" ")[1]


def test_get_photos():

    response = client.get("/photos/")

    assert response.status_code == 200


def test_search_photos():

    response = client.get(
        "/photos/search/?query=test"
    )

    assert response.status_code == 200


def test_filter_by_date():

    response = client.get(
        "/photos/filter/date"
    )

    assert response.status_code == 200


def test_filter_by_rating():

    response = client.get(
        "/photos/filter/rating"
    )

    assert response.status_code == 200


def test_invalid_photo():

    response = client.get(
        "/photos/999999"
    )

    assert response.status_code == 404


def test_create_photo_without_auth():

    response = client.post(
        "/photos/"
    )

    assert response.status_code in [401, 422]


def test_invalid_tags_count():

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post(
        "/photos/",
        headers=headers,
        data={
            "title": "test",
            "description": "test",
            "tags": "1,2,3,4,5,6"
        }
    )

    assert response.status_code in [400, 422]


def test_pagination():

    response = client.get(
        "/photos?page=1&limit=5"
    )

    assert response.status_code == 200