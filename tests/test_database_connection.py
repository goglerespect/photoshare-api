from tests.test_database import (
    TestingSessionLocal
)


def test_testing_database_session():

    db = TestingSessionLocal()

    assert db is not None

    db.close()