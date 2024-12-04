from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from SocialScores.Database.DatabaseFactory import DatabaseFactory
from SocialScores.Models.account import AccountCreate, AccountResponse
from SocialScores.Database.RepositoryAccount import RepositoryAccount

from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()
factory = DatabaseFactory()

db = factory.create(
    type="postgresql",
    db_name=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=int(os.getenv("POSTGRES_PORT"))
)

try:
    db.connect()
except Exception as e:
    print(f"Failed to connect to the database: {e}")
    raise

repo = RepositoryAccount(db)

@router.post("/accounts", response_model=AccountResponse)
def create_account(account: AccountCreate):
    repo.add_account(account)
    return {"username": account.username}

@router.get("/accounts/{username}", response_model=AccountResponse)
def get_account(username: str):
    account = repo.get_account(username)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
