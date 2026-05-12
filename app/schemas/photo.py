from pydantic import BaseModel


class PhotoCreate(BaseModel):

    title: str

    description: str

    image_url: str


class PhotoUpdate(BaseModel):

    title: str

    description: str