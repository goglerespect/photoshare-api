from pydantic import BaseModel
from pydantic import ConfigDict
from typing import List


class PhotoCreate(BaseModel):

    title: str

    description: str

    tags: List[str]


class PhotoUpdate(BaseModel):

    title: str

    description: str


class PhotoResponse(BaseModel):

    id: int

    title: str

    description: str

    image_url: str

    owner_id: int

    tags: List[str]

    model_config = ConfigDict(
        from_attributes = True
    )
