from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from SocialScores.Database.Database import Base  # Import Base from your database module
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# SQLAlchemy ORM Model
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String, nullable=False)  # Reference to the username
    text = Column(Text, nullable=True)
    image = Column(String, nullable=True)
    time_created = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, user: str, text: Optional[str] = None, image: Optional[str] = None):
        self.user = user
        self.text = text
        self.image = image


# Pydantic Schemas
class PostBase(BaseModel):
    user: str
    text: Optional[str] = None
    image: Optional[str] = None

class PostCreate(PostBase):
    id: int

class PostResponse(PostBase):
    time_created: datetime
