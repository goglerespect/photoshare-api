from jose import jwt
from jose import JWTError

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.user import User


# JWT settings
SECRET_KEY = "SUPER_SECRET_KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Bearer auth
oauth2_scheme = HTTPBearer()


# CREATE JWT TOKEN
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# CURRENT USER
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    # Extract token
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid token"
    )

    try:

        # Decode JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Get email from token
        email = payload.get("sub")

        if email is None:

            raise credentials_exception

    except JWTError:

        raise credentials_exception

    # Find user
    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:

        raise credentials_exception

    return user