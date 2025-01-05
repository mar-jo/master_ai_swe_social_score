from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from SocialScores.Database.Database import Base  # Import Base from your database module
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import BaseModel, ConfigDict

# SQLAlchemy ORM Model
class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    socialscore = Column(Integer, default=0)
    profile_image_id = Column(Integer, ForeignKey('images.id'), nullable=True)

    profile_image = relationship("Image")
    posts = relationship("Post", back_populates="account", cascade="all, delete-orphan")

    def __init__(self, email: str, username: str, password: str, socialscore: int = 0):
        self.email = email
        self.username = username
        self.password = password
        self.socialscore = socialscore


# Pydantic Schemas
class AccountBase(BaseModel):
    email: EmailStr
    username: str
    socialscore: Optional[int] = 0

    class Config:
        orm_mode = True  # Allows Pydantic to work with ORM objects

class AccountRegister(BaseModel):
    email: EmailStr
    username: str
    password: str

class AccountCreate(AccountBase):
    password: str

class AccountResponse(AccountBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class AccountLogin(BaseModel):
    username: str
    password: str
