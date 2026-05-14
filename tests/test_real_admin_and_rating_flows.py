from unittest.mock import patch
from io import BytesIO

from tests.conftest import (
    client,
    get_auth_headers,
    get_admin_headers
)


@patch("cloudinary.uploader.upload")
def test_real_rating_success(
    mock_upload
):

    mock_upload.return_value = {
        "secure_url": "https://test.com/photo.jpg",
        "public_id": "photo123"
    }

    # USER 1 CREATES PHOTO
    owner_headers = get_auth_headers()

    fake_image = BytesIO(
        b"fake image"
    )

    create_photo = client.post(
        "/photos/",
        headers=owner_headers,
        files={
            "file": (
                "test.jpg",
                fake_image,
                "image/jpeg"
            )
        },
        data={
            "title": "photo",
            "description": "desc",
            "tags": "nature"
        }
    )

    assert create_photo.status_code in [
        200,
        201
    ]

    photo = create_photo.json()

    photo_id = photo["id"]

    # USER 2 RATES PHOTO
    second_user_headers = get_auth_headers()

    rate = client.post(
        f"/ratings/{photo_id}?value=5",
        headers=second_user_headers
    )

    assert rate.status_code in [
        200,
        201
    ]

    # DUPLICATE
    duplicate = client.post(
        f"/ratings/{photo_id}?value=5",
        headers=second_user_headers
    )

    assert duplicate.status_code == 400


def test_real_admin_success_flow():

    admin_headers = get_admin_headers()

    # CREATE USER
    response = client.post(
        "/auth/register",
        json={
            "email": "target@test.com",
            "username": "target",
            "password": "123456"
        }
    )

    assert response.status_code in [
        200,
        201
    ]

    # SEARCH USER
    search = client.get(
        "/users/search/?query=target",
        headers=admin_headers
    )

    assert search.status_code == 200

    users = search.json()

    target_user = users[0]

    user_id = target_user["id"]

    # BAN
    ban = client.put(
        f"/users/ban/{user_id}",
        headers=admin_headers
    )

    assert ban.status_code == 200

    # UNBAN
    unban = client.put(
        f"/users/unban/{user_id}",
        headers=admin_headers
    )

    assert unban.status_code == 200

    # MAKE MODERATOR
    moderator = client.put(
        f"/users/make-moderator/{user_id}",
        headers=admin_headers
    )

    assert moderator.status_code == 200

    # REMOVE MODERATOR
    remove = client.put(
        f"/users/remove-moderator/{user_id}",
        headers=admin_headers
    )

    assert remove.status_code == 200