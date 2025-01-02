from sqlalchemy import Column, Integer, String
from SocialScores.Database.Database import Base

from pydantic import BaseModel
from typing import Optional

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False, unique=True)
    file_path = Column(String, nullable=False)
    uploader = Column(String, nullable=False)

    def __init__(self, filename: str, file_path: str, uploader: str):
        self.filename = filename
        self.file_path = file_path
        self.uploader = uploader

class ImageBase(BaseModel):
    file_name: str
    description: Optional[str] = None

class ImageCreate(ImageBase):
    pass

class ImageResponse(ImageBase):
    id: int
