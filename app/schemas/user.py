from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import ConfigDict

from typing import Optional


# REGISTER
class UserCreate(BaseModel):

    email: EmailStr

    username: str = Field(
        min_length=3,
        max_length=50
    )

    password: str = Field(
        min_length=6
    )


# LOGIN
class UserLogin(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=1
    )


# UPDATE PROFILE
class UserUpdate(BaseModel):

    username: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50
    )

    bio: Optional[str] = Field(
        default=None,
        max_length=500
    )

    avatar_url: Optional[str] = None


# USER RESPONSE
class UserResponse(BaseModel):

    id: int

    email: EmailStr

    username: str

    bio: Optional[str]

    avatar_url: Optional[str]

    role: str

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )