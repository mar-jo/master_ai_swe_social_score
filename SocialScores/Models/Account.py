from sqlalchemy import Column, Integer, String
from SocialScores.Database.Database import Base  # Import Base from your database module
from pydantic import BaseModel, EmailStr
from typing import Optional

# SQLAlchemy ORM Model
class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)  # Indexed for performance
    username = Column(String, unique=True, nullable=False, index=True)  # Indexed for performance
    password = Column(String, nullable=False)  # Store hashed passwords
    socialscore = Column(Integer, default=0)  # Default social score

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

class AccountLogin(BaseModel):
    username: str
    password: str
