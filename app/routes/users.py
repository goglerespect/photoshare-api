from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.auth import get_current_user

from app.models.user import User

from app.schemas.user import UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# GET MY PROFILE
@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "bio": current_user.bio,
        "avatar_url": current_user.avatar_url,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "photos_count": len(current_user.photos)
    }


# GET USER PROFILE
@router.get("/{username}")
def get_user_profile(
    username: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "username": user.username,
        "bio": user.bio,
        "avatar_url": user.avatar_url,
        "role": user.role,
        "created_at": user.created_at,
        "photos_count": len(user.photos)
    }


# UPDATE MY PROFILE
@router.put("/me")
def update_my_profile(
    body: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if body.username:

        current_user.username = body.username

    if body.bio:

        current_user.bio = body.bio

    if body.avatar_url:

        current_user.avatar_url = body.avatar_url

    db.commit()

    db.refresh(current_user)

    return {
        "message": "Profile updated"
    }


# BAN USER
@router.put("/ban/{user_id}")
def ban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Only admin
    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_active = False

    db.commit()

    db.refresh(user)

    return {
        "message": f"{user.username} banned"
    }


# UNBAN USER
@router.put("/unban/{user_id}")
def unban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Only admin
    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_active = True

    db.commit()

    db.refresh(user)

    return {
        "message": f"{user.username} unbanned"
    }


# MAKE MODERATOR
@router.put("/make-moderator/{user_id}")
def make_moderator(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Only admin
    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.role = "moderator"

    db.commit()

    db.refresh(user)

    return {
        "message": f"{user.username} is now moderator"
    }


# REMOVE MODERATOR
@router.put("/remove-moderator/{user_id}")
def remove_moderator(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Only admin
    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.role = "user"

    db.commit()

    db.refresh(user)

    return {
        "message": f"{user.username} is now user"
    }


# SEARCH USERS
@router.get("/search/")
def search_users(
    query: str,
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

    users = db.query(User).filter(
        User.username.ilike(f"%{query}%")
    ).all()

    return users


# FILTER ACTIVE USERS
@router.get("/filter/active")
def filter_active_users(
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

    users = db.query(User).filter(
        User.is_active == True
    ).all()

    return users


# FILTER BANNED USERS
@router.get("/filter/banned")
def filter_banned_users(
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

    users = db.query(User).filter(
        User.is_active == False
    ).all()

    return users