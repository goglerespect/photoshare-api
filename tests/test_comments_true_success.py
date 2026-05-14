from unittest.mock import patch
from io import BytesIO

from tests.conftest import client
from tests.conftest import get_auth_headers


@patch("cloudinary.uploader.upload")
def test_comment_true_success_flow(
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
    create_comment = client.post(
        f"/comments/{photo_id}",
        headers=headers,
        json={
            "text": "hello"
        }
    )

    assert create_comment.status_code in [
        200,
        201
    ]

    comment = create_comment.json()

    comment_id = comment["id"]

    # UPDATE COMMENT
    update_comment = client.put(
        f"/comments/{comment_id}",
        headers=headers,
        json={
            "text": "updated"
        }
    )

    assert update_comment.status_code == 200