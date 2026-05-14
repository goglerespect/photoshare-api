from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.core.database import Base


class Transformation(Base):

    __tablename__ = "transformations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    transformed_url = Column(
        String,
        nullable=False
    )

    qr_code_url = Column(
        String,
        nullable=False
    )

    transformation_type = Column(
        String,
        nullable=False
    )

    photo_id = Column(
        Integer,
        ForeignKey("photos.id")
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    photo = relationship(
        "Photo"
    )

    owner = relationship(
        "User"
    )