from pydantic import BaseModel

class AccountCreate(BaseModel):
    username: str

class AccountResponse(AccountCreate):
    id: int

    class Config:
        orm_mode = True
