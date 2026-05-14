from app.core.auth import (
    create_access_token
)


def test_create_access_token():

    token = create_access_token(
        {"sub": "test@test.com"}
    )

    assert token is not None