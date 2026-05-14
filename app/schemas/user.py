from pydantic import BaseModel
from pydantic import EmailStr


# Реєстрація
class UserCreate(BaseModel):

    email: EmailStr

    username: str

    password: str


# Login
class UserLogin(BaseModel):

    email: EmailStr

    password: str

# Update profile
class UserUpdate(BaseModel):

    username: str | None = None

    bio: str | None = None

    avatar_url: str | None = None