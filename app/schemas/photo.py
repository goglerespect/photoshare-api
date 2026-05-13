from pydantic import BaseModel


class PhotoCreate(BaseModel):

    title: str

    description: str


class PhotoUpdate(BaseModel):

    title: str

    description: str