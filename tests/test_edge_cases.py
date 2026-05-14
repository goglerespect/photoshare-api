from tests.conftest import client
from tests.conftest import get_auth_headers


def test_invalid_photo_page():

    response = client.get(
        "/photos?page=-1&limit=5"
    )

    assert response.status_code == 422


def test_invalid_photo_limit():

    response = client.get(
        "/photos?page=1&limit=500"
    )

    assert response.status_code == 422


def test_invalid_rating_type():

    headers = get_auth_headers()

    response = client.post(
        "/ratings/1?value=text",
        headers=headers
    )

    assert response.status_code == 422


def test_search_tag_not_found():

    response = client.get(
        "/photos/tag/not_existing_tag"
    )

    assert response.status_code == 200


def test_users_search_without_query():

    headers = get_auth_headers()

    response = client.get(
        "/users/search/",
        headers=headers
    )

    assert response.status_code == 422