from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db

from app.core.auth import get_current_user

from app.models.user import User
from app.models.photo import Photo
from app.models.rating import Rating


router = APIRouter(
    prefix="/ratings",
    tags=["ratings"]
)


# CREATE RATING
@router.post("/{photo_id}")
def rate_photo(
    photo_id: int,
    value: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Validate rating
    if value < 1 or value > 5:

        raise HTTPException(
            status_code=400,
            detail="Rating must be between 1 and 5"
        )

    photo = db.query(Photo).filter(
        Photo.id == photo_id
    ).first()

    if not photo:

        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    # Cannot rate own photo
    if photo.owner_id == current_user.id:

        raise HTTPException(
            status_code=400,
            detail="You cannot rate your own photo"
        )

    # Check existing rating
    existing_rating = db.query(Rating).filter(
        Rating.photo_id == photo_id,
        Rating.user_id == current_user.id
    ).first()

    if existing_rating:

        raise HTTPException(
            status_code=400,
            detail="You already rated this photo"
        )

    rating = Rating(
        value=value,
        photo_id=photo_id,
        user_id=current_user.id
    )

    db.add(rating)

    db.commit()

    db.refresh(rating)

    return {
        "message": "Rating added",
        "rating": rating.value
    }


# GET PHOTO RATING
@router.get("/{photo_id}")
def get_photo_rating(
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

    avg_rating = db.query(
        func.avg(Rating.value)
    ).filter(
        Rating.photo_id == photo_id
    ).scalar()

    total_ratings = db.query(Rating).filter(
        Rating.photo_id == photo_id
    ).count()

    return {
        "photo_id": photo_id,
        "average_rating": round(avg_rating, 2)
        if avg_rating else 0,
        "total_ratings": total_ratings
    }


# GET ALL RATINGS FOR PHOTO
@router.get("/photo/{photo_id}")
def get_photo_ratings(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Only moderator/admin
    if current_user.role not in [
        "moderator",
        "admin"
    ]:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    ratings = db.query(Rating).filter(
        Rating.photo_id == photo_id
    ).all()

    return ratings


# DELETE RATING
@router.delete("/{rating_id}")
def delete_rating(
    rating_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Only moderator/admin
    if current_user.role not in [
        "moderator",
        "admin"
    ]:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    rating = db.query(Rating).filter(
        Rating.id == rating_id
    ).first()

    if not rating:

        raise HTTPException(
            status_code=404,
            detail="Rating not found"
        )

    db.delete(rating)

    db.commit()

    return {
        "message": "Rating deleted"
    }