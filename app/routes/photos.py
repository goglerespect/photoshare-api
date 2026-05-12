from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.auth import get_current_user

from app.models.user import User
from app.models.photo import Photo

from app.schemas.photo import PhotoCreate


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