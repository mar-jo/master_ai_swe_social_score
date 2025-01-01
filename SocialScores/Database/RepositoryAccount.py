from sqlalchemy.orm import Session
from SocialScores.Models.Account import Account
from passlib.hash import bcrypt

table_name = "accounts"
columns = {
    "id": "SERIAL PRIMARY KEY",
    "email": "VARCHAR(255) UNIQUE NOT NULL",
    "username": "VARCHAR(255) UNIQUE NOT NULL",
    "password": "VARCHAR(255) NOT NULL",
    "socialscore": "INTEGER DEFAULT 0",
}

class RepositoryAccount:
    def __init__(self, db: Session):
        self.db = db

    def create_account(self, email: str, username: str, password: str):
        if self.db.query(Account).filter_by(email=email).first():
            raise ValueError("Email already registered")
        if self.db.query(Account).filter_by(username=username).first():
            raise ValueError("Username already taken")

        hashed_password = bcrypt.hash(password)
        new_account = Account(email=email, username=username, password=hashed_password)
        self.db.add(new_account)
        self.db.commit()
        self.db.refresh(new_account)
        return new_account

    def validate_login(self, username: str, password: str):
        account = self.db.query(Account).filter_by(username=username).first()
        if account and bcrypt.verify(password, account.password):  # Verify hashed password
            return account
        raise ValueError("Invalid username or password")
