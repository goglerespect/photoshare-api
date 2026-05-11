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