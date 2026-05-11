from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean

from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String, unique=True)

    username = Column(String, unique=True)

    password = Column(String)

    role = Column(String, default="user")

    is_active = Column(Boolean, default=True)