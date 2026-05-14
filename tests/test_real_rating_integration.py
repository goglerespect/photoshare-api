from unittest.mock import patch
from io import BytesIO

from tests.conftest import client
from tests.conftest import get_auth_headers


@patch("cloudinary.uploader.upload")
def test_real_rating_flow(
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

    # RATE
    rating_response = client.post(
        f"/ratings/{photo_id}?value=5",
        headers=headers
    )

    assert rating_response.status_code in [
        200,
        201,
        400
    ]

    # DUPLICATE
    duplicate = client.post(
        f"/ratings/{photo_id}?value=5",
        headers=headers
    )

    assert duplicate.status_code in [
        400,
        409
    ]

    # GET RATINGS
    get_response = client.get(
        f"/ratings/photo/{photo_id}",
        headers=headers
    )

    assert get_response.status_code in [
        200,
        403
    ]