from pydantic import BaseModel

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

    class Config:

        from_attributes = True