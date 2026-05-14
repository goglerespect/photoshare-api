from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import File
from fastapi import Form

from sqlalchemy.orm import Session

import cloudinary
import cloudinary.uploader

import qrcode
import uuid

# Cloudinary config
import app.core.cloudinary

from app.core.database import get_db

from app.core.auth import get_current_user

from app.models.user import User
from app.models.photo import Photo
from app.models.tag import Tag
from app.models.transformation import Transformation

from app.schemas.photo import PhotoUpdate


router = APIRouter(
    prefix="/photos",
    tags=["photos"]
)


# CREATE PHOTO
@router.post("/")
def create_photo(
    title: str = Form(...),
    description: str = Form(...),
    tags: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Convert tags string to list
    tags_list = []

    if tags:

        tags_list = [
            tag.strip().lower()
            for tag in tags.split(",")
        ]

    # Max 5 tags
    if len(tags_list) > 5:

        raise HTTPException(
            status_code=400,
            detail="Maximum 5 tags allowed"
        )

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

    # Add tags
    for tag_name in tags_list:

        tag = db.query(Tag).filter(
            Tag.name == tag_name
        ).first()

        # Create tag if not exists
        if not tag:

            tag = Tag(
                name=tag_name
            )

            db.add(tag)

            db.commit()

            db.refresh(tag)

        photo.tags.append(tag)

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
        "tags": tags_list,
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
        "owner_id": photo.owner_id,
        "tags": [tag.name for tag in photo.tags]
    }


# SEARCH PHOTOS BY TAG
@router.get("/tag/{tag_name}")
def get_photos_by_tag(
    tag_name: str,
    db: Session = Depends(get_db)
):

    photos = db.query(Photo).join(
        Photo.tags
    ).filter(
        Tag.name == tag_name.lower()
    ).all()

    return photos


# CREATE TRANSFORMATION + QR
@router.post("/transform/{photo_id}")
def create_transformation(
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

    # Get Cloudinary public ID
    public_id = photo.image_url.split("/")[-1].split(".")[0]

    # Generate transformed image URL
    transformed_url = cloudinary.CloudinaryImage(
        public_id
    ).build_url(
        width=500,
        height=500,
        crop="fill",
        effect="grayscale"
    )

    # Generate QR code
    qr = qrcode.make(transformed_url)

    filename = f"{uuid.uuid4()}.png"

    qr_path = f"uploads/qr/{filename}"

    qr.save(qr_path)

    qr_code_url = f"/uploads/qr/{filename}"

    # Save transformation
    transformation = Transformation(
        transformed_url=transformed_url,
        qr_code_url=qr_code_url,
        transformation_type="grayscale",
        photo_id=photo.id,
        owner_id=current_user.id
    )

    db.add(transformation)

    db.commit()

    db.refresh(transformation)

    return {
        "id": transformation.id,
        "transformed_url": transformation.transformed_url,
        "qr_code_url": transformation.qr_code_url
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