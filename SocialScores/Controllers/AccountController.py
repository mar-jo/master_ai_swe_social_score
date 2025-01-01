from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from SocialScores.Database.RepositoryAccount import RepositoryAccount
from SocialScores.Models.Account import AccountRegister, AccountLogin, AccountResponse
from SocialScores.Database.Database import get_db

class AccountController:
    def __init__(self, db: Session):
        self.repo = RepositoryAccount(db)

    def register(self, account: AccountRegister):
        try:
            new_account = self.repo.create_account(
                email=account.email,
                username=account.username,
                password=account.password
            )
            return {"message": "Account registered successfully", "id": new_account.id}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def login(self, account: AccountLogin):
        try:
            account = self.repo.validate_login(account.username, account.password)
            return {"message": "Login successful", "id": account.id}
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

router = APIRouter()

@router.post("/register")
def register(account: AccountRegister, db: Session = Depends(get_db)):
    controller = AccountController(db)
    return controller.register(account)

@router.post("/login")
def login(account: AccountLogin, db: Session = Depends(get_db)):
    controller = AccountController(db)
    return controller.login(account)
