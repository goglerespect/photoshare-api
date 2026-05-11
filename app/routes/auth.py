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

    # Перевірка email
    existing_email = db.query(User).filter(
        User.email == body.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    # Перевірка username
    existing_username = db.query(User).filter(
        User.username == body.username
    ).first()

    if existing_username:

        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    # Хешуємо пароль
    hashed_password = hash_password(
        body.password
    )

    # Створення user
    user = User(
        email=body.email,
        username=body.username,
        password=hashed_password
    )

    db.add(user)

    db.commit()

    return {
        "message": "User created"
    }


# LOGIN
@router.post("/login")
def login(
    body: UserLogin,
    db: Session = Depends(get_db)
):

    # Шукаємо користувача
    user = db.query(User).filter(
        User.email == body.email
    ).first()

    # Якщо користувача нема
    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Перевірка пароля
    valid_password = verify_password(
        body.password,
        user.password
    )

    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Генерація JWT
    access_token = create_access_token({
        "sub": user.email
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }