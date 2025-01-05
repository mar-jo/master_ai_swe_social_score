from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func, ForeignKey
from fastapi import UploadFile
from sqlalchemy.orm import relationship
from SocialScores.Database.Database import Base  # Import Base from your database module
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# SQLAlchemy ORM Model
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.id', ondelete="CASCADE"), nullable=False)
    user = Column(String, nullable=False)
    text = Column(Text, nullable=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=True)
    time_created = Column(TIMESTAMP, server_default=func.now())

    account = relationship("Account", back_populates="posts")
    image = relationship("Image", back_populates="post")

    def __init__(self, user: str, account_id: int, text: Optional[str] = None, image_id: Optional[int] = None):
        self.user = user
        self.account_id = account_id
        self.text = text
        self.image_id = image_id

# Pydantic Schemas
class PostBase(BaseModel):
    user: str
    account_id: int
    text: str = None
    image: Optional[UploadFile] = None

class PostCreate(PostBase):
    id: int

class PostResponse(PostBase):
    time_created: datetime

    model_config = ConfigDict(from_attributes=True)
