from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import relationship

from app.core.database import Base


class Rating(Base):

    __tablename__ = "ratings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    value = Column(
        Integer,
        nullable=False
    )

    photo_id = Column(
        Integer,
        ForeignKey("photos.id")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    # One rating per user per photo
    __table_args__ = (
        UniqueConstraint(
            "photo_id",
            "user_id",
            name="unique_user_photo_rating"
        ),
    )

    photo = relationship(
        "Photo"
    )

    user = relationship(
        "User"
    )