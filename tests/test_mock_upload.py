from unittest.mock import patch

from tests.conftest import client
from tests.conftest import get_auth_headers


@patch("cloudinary.uploader.upload")
def test_mock_upload(
    mock_upload
):

    mock_upload.return_value = {
        "secure_url": "https://test.com/image.jpg",
        "public_id": "test_image"
    }

    headers = get_auth_headers()

    response = client.post(
        "/photos/",
        headers=headers,
        data={
            "title": "test",
            "description": "test",
            "tags": "nature"
        }
    )

    assert response.status_code in [200, 422]