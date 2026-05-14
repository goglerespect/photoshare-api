import sys
import os
import uuid

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import pytest

from fastapi.testclient import TestClient

from app.main import app

from app.core.database import (
    Base,
    get_db
)

from tests.test_database import (
    TestingSessionLocal,
    engine
)

from app.models.user import User


# CREATE TEST TABLES
Base.metadata.create_all(
    bind=engine
)


# OVERRIDE DATABASE
def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[get_db] = (
    override_get_db
)


client = TestClient(app)


# CLEAN DATABASE AFTER EACH TEST
@pytest.fixture(autouse=True)
def cleanup_db():

    yield

    db = TestingSessionLocal()

    for table in reversed(
        Base.metadata.sorted_tables
    ):
        db.execute(table.delete())

    db.commit()

    db.close()


# CREATE RANDOM USER
def create_random_user(
    role: str = "user"
):

    unique_id = str(uuid.uuid4())[:8]

    user = {
        "email": f"{unique_id}@test.com",
        "username": f"user_{unique_id}",
        "password": "123456"
    }

    # Register
    register_response = client.post(
        "/auth/register",
        json=user
    )

    # Update role if needed
    if role != "user":

        db = TestingSessionLocal()

        created_user = db.query(User).filter(
            User.email == user["email"]
        ).first()

        if created_user:

            created_user.role = role

            db.commit()

        db.close()

    return user


# GET AUTH HEADERS
def get_auth_headers():

    user = create_random_user()

    login = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "password": user["password"]
        }
    )

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# GET ADMIN HEADERS
def get_admin_headers():

    user = create_random_user(
        role="admin"
    )

    login = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "password": user["password"]
        }
    )

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# GET MODERATOR HEADERS
def get_moderator_headers():

    user = create_random_user(
        role="moderator"
    )

    login = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "password": user["password"]
        }
    )

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# DEFAULT TEST USER FIXTURE
@pytest.fixture
def test_user():

    return create_random_user()