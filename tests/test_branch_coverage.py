from tests.conftest import client
from tests.conftest import get_auth_headers


# ---------- USERS ----------

def test_get_me_without_auth():

    response = client.get(
        "/users/me"
    )

    assert response.status_code in [401, 403]


def test_update_profile_without_auth():

    response = client.put(
        "/users/me",
        json={
            "bio": "test"
        }
    )

    assert response.status_code in [401, 403]


def test_search_users_without_auth():

    response = client.get(
        "/users/search/?query=test"
    )

    assert response.status_code in [401, 403]


# ---------- PHOTOS ----------

def test_update_photo_without_auth():

    response = client.put(
        "/photos/1",
        json={
            "title": "updated",
            "description": "updated"
        }
    )

    assert response.status_code in [401, 403]


def test_delete_photo_without_auth():

    response = client.delete(
        "/photos/1"
    )

    assert response.status_code in [401, 403]


def test_transform_photo_without_auth():

    response = client.post(
        "/photos/transform/1"
    )

    assert response.status_code in [401, 403]


def test_get_photo_not_found():

    response = client.get(
        "/photos/999999"
    )

    assert response.status_code == 404


# ---------- COMMENTS ----------

def test_create_comment_without_auth():

    response = client.post(
        "/comments/1",
        json={
            "text": "test"
        }
    )

    assert response.status_code in [401, 403]


def test_edit_comment_without_auth():

    response = client.put(
        "/comments/1",
        json={
            "text": "updated"
        }
    )

    assert response.status_code in [401, 403]


def test_delete_comment_without_auth():

    response = client.delete(
        "/comments/1"
    )

    assert response.status_code in [401, 403]


# ---------- RATINGS ----------

def test_create_rating_without_auth():

    response = client.post(
        "/ratings/1?value=5"
    )

    assert response.status_code in [401, 403]


def test_delete_rating_without_auth():

    response = client.delete(
        "/ratings/1"
    )

    assert response.status_code in [401, 403]


def test_invalid_rating_large():

    headers = get_auth_headers()

    response = client.post(
        "/ratings/1?value=100",
        headers=headers
    )

    assert response.status_code == 400


def test_invalid_rating_small():

    headers = get_auth_headers()

    response = client.post(
        "/ratings/1?value=-1",
        headers=headers
    )

    assert response.status_code == 400


# ---------- SEARCH/FILTER ----------

def test_empty_search_query():

    response = client.get(
        "/photos/search/?query="
    )

    assert response.status_code == 200


def test_unknown_tag():

    response = client.get(
        "/photos/tag/unknown_tag"
    )

    assert response.status_code == 200


def test_invalid_pagination():

    response = client.get(
        "/photos?page=-1&limit=500"
    )

    assert response.status_code == 422