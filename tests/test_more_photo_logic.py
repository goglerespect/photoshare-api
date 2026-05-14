from tests.conftest import client


def test_filter_rating():

    response = client.get(
        "/photos/filter/rating"
    )

    assert response.status_code == 200


def test_filter_date():

    response = client.get(
        "/photos/filter/date"
    )

    assert response.status_code == 200


def test_search_photos_empty():

    response = client.get(
        "/photos/search/?query="
    )

    assert response.status_code == 200


def test_get_nonexistent_tag():

    response = client.get(
        "/photos/tag/unknown_tag"
    )

    assert response.status_code == 200