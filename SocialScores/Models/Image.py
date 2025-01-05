from sqlalchemy import Column, Integer, String, LargeBinary, TIMESTAMP, func
from SocialScores.Database.Database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# SQLAlchemy ORM Model
class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    binary_data = Column(LargeBinary, nullable=False)  # Store binary data
    uploader = Column(String, nullable=False)
    time_created = Column(TIMESTAMP, server_default=func.now())

    post = relationship("Post", back_populates="image")

    def __init__(self, filename: str, binary_data: bytes, uploader: str):
        self.filename = filename
        self.binary_data = binary_data
        self.uploader = uploader

# Pydantic Schemas
class ImageBase(BaseModel):
    filename: str
    binary_data: bytes
    uploader: str

class ImageCreate(ImageBase):
    id: int

class ImageResponse(ImageBase):
    time_created: datetime

    model_config = ConfigDict(from_attributes=True)
