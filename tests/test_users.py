from tests.conftest import client


def test_me_without_auth():

    response = client.get(
        "/users/me"
    )

    assert response.status_code in [401, 403]


def test_search_users_without_auth():

    response = client.get(
        "/users/search/?query=test"
    )

    assert response.status_code in [401, 403]


def test_filter_active_users_without_auth():

    response = client.get(
        "/users/filter/active"
    )

    assert response.status_code in [401, 403]


def test_filter_banned_users_without_auth():

    response = client.get(
        "/users/filter/banned"
    )

    assert response.status_code in [401, 403]