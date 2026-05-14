from unittest.mock import patch
from io import BytesIO

from tests.conftest import client
from tests.conftest import get_auth_headers


@patch("cloudinary.uploader.upload")
def test_real_comment_flow(
    mock_upload
):

    mock_upload.return_value = {
        "secure_url": "https://test.com/photo.jpg",
        "public_id": "photo123"
    }

    headers = get_auth_headers()

    fake_image = BytesIO(
        b"fake image"
    )

    # CREATE PHOTO
    photo_response = client.post(
        "/photos/",
        headers=headers,
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

    assert photo_response.status_code in [
        200,
        201
    ]

    photo = photo_response.json()

    photo_id = photo["id"]

    # CREATE COMMENT
    comment_response = client.post(
        f"/comments/{photo_id}",
        headers=headers,
        json={
            "text": "hello"
        }
    )

    assert comment_response.status_code in [
        200,
        201
    ]

    comment = comment_response.json()

    comment_id = comment["id"]

    # UPDATE COMMENT
    update_response = client.put(
        f"/comments/{comment_id}",
        headers=headers,
        json={
            "text": "updated"
        }
    )

    assert update_response.status_code == 200

    # DELETE COMMENT
    delete_response = client.delete(
        f"/comments/{comment_id}",
        headers=headers
    )

    assert delete_response.status_code == 200