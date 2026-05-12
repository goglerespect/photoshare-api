from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean

from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    # Primary key
    id = Column(
        Integer,
        primary_key=True
    )

    # User email
    email = Column(
        String,
        unique=True,
        nullable=False
    )

    # Username
    username = Column(
        String,
        unique=True,
        nullable=False
    )

    # Hashed password
    password = Column(
        String,
        nullable=False
    )

    # Roles:
    # user / moderator / admin
    role = Column(
        String,
        default="user"
    )

    # Ban system
    is_active = Column(
        Boolean,
        default=True
    )

    # User photos
    photos = relationship(
        "Photo",
        back_populates="owner"
    )