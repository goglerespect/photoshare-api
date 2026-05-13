from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from app.core.database import Base


photo_tags = Table(
    "photo_tags",
    Base.metadata,

    Column(
        "photo_id",
        Integer,
        ForeignKey("photos.id")
    ),

    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id")
    )
)