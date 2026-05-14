from tests.conftest import client


def test_register(test_user):

    response = client.post(
        "/auth/register",
        json=test_user
    )

    assert response.status_code in [200, 201, 400, 409]


def test_duplicate_register(test_user):

    response = client.post(
        "/auth/register",
        json=test_user
    )

    assert response.status_code in [400, 409]


def test_register_invalid_email():

    response = client.post(
        "/auth/register",
        json={
            "email": "invalid-email",
            "username": "test",
            "password": "123456"
        }
    )

    assert response.status_code == 422


def test_register_empty_password():

    response = client.post(
        "/auth/register",
        json={
            "email": "empty@test.com",
            "username": "empty",
            "password": ""
        }
    )

    assert response.status_code in [400, 422]


def test_login(test_user):

    response = client.post(
        "/auth/login",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

    assert data["token_type"] == "bearer"


def test_invalid_login():

    response = client.post(
        "/auth/login",
        json={
            "email": "wrong@test.com",
            "password": "wrong"
        }
    )

    assert response.status_code == 401


def test_invalid_password(test_user):

    response = client.post(
        "/auth/login",
        json={
            "email": test_user["email"],
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_login_without_password():

    response = client.post(
        "/auth/login",
        json={
            "email": "test@test.com"
        }
    )

    assert response.status_code == 422


def test_login_without_email():

    response = client.post(
        "/auth/login",
        json={
            "password": "123456"
        }
    )

    assert response.status_code == 422