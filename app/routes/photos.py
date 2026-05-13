from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import File

from sqlalchemy.orm import Session

import cloudinary
import cloudinary.uploader

# Cloudinary config
import app.core.cloudinary

from app.core.database import get_db

from app.core.auth import get_current_user

from app.models.user import User
from app.models.photo import Photo

from app.schemas.photo import PhotoUpdate


router = APIRouter(
    prefix="/photos",
    tags=["photos"]
)


# CREATE PHOTO
@router.post("/")
def create_photo(
    title: str,
    description: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Upload image to Cloudinary
    upload_result = cloudinary.uploader.upload(
        file.file,

        cloud_name=app.core.cloudinary.CLOUD_NAME,

        api_key=app.core.cloudinary.API_KEY,

        api_secret=app.core.cloudinary.API_SECRET
    )

    # Original image URL
    image_url = upload_result["secure_url"]

    # Cloudinary public ID
    public_id = upload_result["public_id"]

    # Thumbnail URL
    thumbnail_url = cloudinary.CloudinaryImage(
        public_id
    ).build_url(
        width=300,
        height=300,
        crop="fill"
    )

    # Create photo object
    photo = Photo(
        title=title,
        description=description,
        image_url=image_url,
        owner_id=current_user.id
    )

    # Save to database
    db.add(photo)

    db.commit()

    db.refresh(photo)

    return {
        "id": photo.id,
        "title": photo.title,
        "description": photo.description,
        "image_url": photo.image_url,
        "thumbnail_url": thumbnail_url,
        "owner_id": photo.owner_id
    }


# GET PHOTO
@router.get("/{photo_id}")
def get_photo(
    photo_id: int,
    db: Session = Depends(get_db)
):

    photo = db.query(Photo).filter(
        Photo.id == photo_id
    ).first()

    if not photo:

        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    return {
        "id": photo.id,
        "title": photo.title,
        "description": photo.description,
        "image_url": photo.image_url,
        "owner_id": photo.owner_id
    }


# UPDATE PHOTO
@router.put("/{photo_id}")
def update_photo(
    photo_id: int,
    body: PhotoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    photo = db.query(Photo).filter(
        Photo.id == photo_id
    ).first()

    if not photo:

        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    # Only owner or admin
    if (
        photo.owner_id != current_user.id
        and current_user.role != "admin"
    ):

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    # Update photo
    photo.title = body.title

    photo.description = body.description

    db.commit()

    db.refresh(photo)

    return {
        "message": "Photo updated"
    }


# DELETE PHOTO
@router.delete("/{photo_id}")
def delete_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    photo = db.query(Photo).filter(
        Photo.id == photo_id
    ).first()

    if not photo:

        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    # Only owner or admin
    if (
        photo.owner_id != current_user.id
        and current_user.role != "admin"
    ):

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    db.delete(photo)

    db.commit()

    return {
        "message": "Photo deleted"
    }