from unittest.mock import patch
from io import BytesIO

from tests.conftest import client
from tests.conftest import get_auth_headers


@patch("cloudinary.uploader.upload")
def test_create_photo_success(
    mock_upload
):

    mock_upload.return_value = {
        "secure_url": "https://test.com/photo.jpg",
        "public_id": "photo123"
    }

    headers = get_auth_headers()

    fake_image = BytesIO(
        b"fake image content"
    )

    response = client.post(
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
            "title": "nature",
            "description": "beautiful",
            "tags": "nature,forest"
        }
    )

    assert response.status_code in [200, 201]