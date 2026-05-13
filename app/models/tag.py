from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.photo_tag import photo_tags


class Tag(Base):

    __tablename__ = "tags"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    photos = relationship(
        "Photo",
        secondary=photo_tags,
        back_populates="tags"
    )