from app.core.security import (
    hash_password,
    verify_password
)


def test_hash_password():

    password = "123456"

    hashed = hash_password(password)

    assert hashed != password


def test_verify_password():

    password = "123456"

    hashed = hash_password(password)

    assert verify_password(
        password,
        hashed
    ) is True