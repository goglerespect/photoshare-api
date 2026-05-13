from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.auth import get_current_user

from app.models.user import User
from app.models.photo import Photo
from app.models.comment import Comment

from app.schemas.comment import CommentCreate
from app.schemas.comment import CommentUpdate


router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)


# CREATE COMMENT
@router.post("/{photo_id}")
def create_comment(
    photo_id: int,
    body: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Check photo exists
    photo = db.query(Photo).filter(
        Photo.id == photo_id
    ).first()

    if not photo:

        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    # Create comment
    comment = Comment(
        text=body.text,
        owner_id=current_user.id,
        photo_id=photo.id
    )

    db.add(comment)

    db.commit()

    db.refresh(comment)

    return {
        "id": comment.id,
        "text": comment.text,
        "photo_id": comment.photo_id,
        "owner_id": comment.owner_id
    }


# GET COMMENTS BY PHOTO
@router.get("/photo/{photo_id}")
def get_photo_comments(
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

    comments = db.query(Comment).filter(
        Comment.photo_id == photo_id
    ).all()

    return comments


# UPDATE COMMENT
@router.put("/{comment_id}")
def update_comment(
    comment_id: int,
    body: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()

    if not comment:

        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    # Only owner can update
    if comment.owner_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    comment.text = body.text

    db.commit()

    db.refresh(comment)

    return {
        "message": "Comment updated"
    }


# DELETE COMMENT
@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()

    if not comment:

        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    # Owner or admin
    if (
        comment.owner_id != current_user.id
        and current_user.role != "admin"
    ):

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    db.delete(comment)

    db.commit()

    return {
        "message": "Comment deleted"
    }