from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="user"
    )

    # User active status
    is_active = Column(
        Boolean,
        default=True
    )

    # User bio
    bio = Column(
        String,
        nullable=True
    )

    # Avatar URL
    avatar_url = Column(
        String,
        nullable=True
    )

    # Registration date
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relations
    photos = relationship(
        "Photo",
        back_populates="owner"
    )

    comments = relationship(
        "Comment",
        back_populates="owner"
    )