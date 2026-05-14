from unittest.mock import patch
from io import BytesIO

from tests.conftest import client
from tests.conftest import get_auth_headers


@patch("cloudinary.uploader.upload")
def test_photo_full_lifecycle(
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

    # CREATE
    create_response = client.post(
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

    assert create_response.status_code in [200, 201]

    photo_data = create_response.json()

    photo_id = photo_data["id"]

    # GET
    get_response = client.get(
        f"/photos/{photo_id}"
    )

    assert get_response.status_code == 200

    # UPDATE
    update_response = client.put(
        f"/photos/{photo_id}",
        headers=headers,
        json={
            "title": "updated",
            "description": "updated"
        }
    )

    assert update_response.status_code == 200

    # DELETE
    delete_response = client.delete(
        f"/photos/{photo_id}",
        headers=headers
    )

    assert delete_response.status_code == 200