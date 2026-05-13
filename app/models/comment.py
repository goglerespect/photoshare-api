from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.core.database import Base


class Comment(Base):

    __tablename__ = "comments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    text = Column(
        String,
        nullable=False
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    photo_id = Column(
        Integer,
        ForeignKey("photos.id")
    )

    owner = relationship(
        "User",
        back_populates="comments"
    )

    photo = relationship(
        "Photo",
        back_populates="comments"
    )