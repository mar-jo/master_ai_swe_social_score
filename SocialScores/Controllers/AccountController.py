from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from SocialScores.Database.RepositoryAccount import RepositoryAccount
from SocialScores.Models.Account import AccountRegister, AccountLogin
from SocialScores.Database.Database import get_db

router = APIRouter()

@router.post("/register")
def register(account: AccountRegister, db: Session = Depends(get_db)):
    """
    Register a new account.
    """
    repo = RepositoryAccount(db)
    try:
        new_account = repo.create_account(
            email=account.email, username=account.username, password=account.password
        )
        return {"message": "Account created successfully", "account": new_account}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(account: AccountLogin, db: Session = Depends(get_db)):
    """
    Log in to an account.
    """
    repo = RepositoryAccount(db)
    try:
        user = repo.validate_login(username=account.username, password=account.password)
        return {"message": "Login successful", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
