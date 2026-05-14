from unittest.mock import patch

from tests.conftest import client
from tests.conftest import get_auth_headers


@patch("cloudinary.uploader.upload")
def test_transform_nonexistent(
    mock_upload
):

    mock_upload.return_value = {
        "secure_url": "https://test.com/photo.jpg",
        "public_id": "photo123"
    }

    headers = get_auth_headers()

    response = client.post(
        "/photos/transform/999999",
        headers=headers
    )

    assert response.status_code == 404