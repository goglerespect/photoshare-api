from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.user import User

from app.schemas.user import UserCreate
from app.schemas.user import UserLogin

from app.core.security import hash_password
from app.core.security import verify_password

from app.core.auth import create_access_token
from app.core.auth import get_current_user


# ROUTER
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# REGISTER
@router.post("/register")
def register(
    body: UserCreate,
    db: Session = Depends(get_db)
):

    existing_email = db.query(User).filter(
        User.email == body.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    existing_username = db.query(User).filter(
        User.username == body.username
    ).first()

    if existing_username:

        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    hashed_password = hash_password(
        body.password
    )
    # Рахуємо користувачів
    users_count = db.query(User).count()

    # Перший user = admin
    role = "admin" if users_count == 0 else "user"

    user = User(
    email=body.email,
    username=body.username,
    password=hashed_password,
    role=role
    )
    

    db.add(user)

    db.commit()

    db.refresh(user)

    return {
        "message": "User created"
    }


# LOGIN
@router.post("/login")
def login(
    body: UserLogin,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == body.email
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    valid_password = verify_password(
        body.password,
        user.password
    )

    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token({
        "sub": user.email
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# CURRENT USER
@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "role": current_user.role
    }