from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.photo_tag import photo_tags


class Photo(Base):

    __tablename__ = "photos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=False
    )

    image_url = Column(
        String,
        nullable=False
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    # Photo creation date
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Photo owner
    owner = relationship(
        "User",
        back_populates="photos"
    )

    # Photo comments
    comments = relationship(
        "Comment",
        back_populates="photo"
    )

    # Photo tags
    tags = relationship(
        "Tag",
        secondary=photo_tags,
        back_populates="photos"
    )