from tests.test_database import (
    TestingSessionLocal
)


def test_database_connection():

    db = TestingSessionLocal()

    assert db is not None

    db.close()