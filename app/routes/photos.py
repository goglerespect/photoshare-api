from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.auth import get_current_user

from app.models.user import User
from app.models.photo import Photo

from app.schemas.photo import PhotoCreate
from app.schemas.photo import PhotoUpdate


router = APIRouter(
    prefix="/photos",
    tags=["photos"]
)


# CREATE PHOTO
@router.post("/")
def create_photo(
    body: PhotoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    photo = Photo(
        title=body.title,
        description=body.description,
        image_url=body.image_url,
        owner_id=current_user.id
    )

    db.add(photo)

    db.commit()

    db.refresh(photo)

    return {
        "id": photo.id,
        "title": photo.title,
        "description": photo.description,
        "image_url": photo.image_url,
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

    # Update data
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