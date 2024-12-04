from pydantic import BaseModel
from typing import Optional

class PostCreate(BaseModel):
    username: str
    image: Optional[str] = None

class PostResponse(PostCreate):
    id: int

    class Config:
        orm_mode = True
