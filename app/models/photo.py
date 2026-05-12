from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base


class Photo(Base):

    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)

    title = Column(String)

    description = Column(String)

    image_url = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    # Relationship
    owner = relationship(
        "User",
        back_populates="photos"
    )