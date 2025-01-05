from sqlalchemy.orm import Session
from SocialScores.Models.Account import Account
from SocialScores.Models.Post import Post
from passlib.hash import bcrypt
from typing import Optional, List, cast
from random import sample

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
        if account and bcrypt.verify(password, account.password):
            return account

        raise ValueError("Invalid username or password")

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        return self.db.query(Account).filter(Account.id == account_id).first()

    def get_accounts_random(self, count: int) -> List[Account]:
        accounts = cast(List[Account], self.db.query(Account).all())
        if count >= len(accounts):
            return accounts
        return sample(accounts, count)

    def get_posts_for_account(self, account_id: int) -> List:
        return self.db.query(Post).filter(Post.user_id == account_id).all()

    def get_highscores(self, limit: int = 10):
        return self.db.query(Account).order_by(Account.socialscore.desc()).limit(limit).all()

    def update_socialscore(self, account_id: int, delta: int):
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise ValueError("Account not found")

        account.socialscore += delta
        self.db.commit()
        self.db.refresh(account)
        return account

    def update_profile_image(self, account_id: int, image_id: int):
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise ValueError("Account not found")
        account.profile_image_id = image_id
        self.db.commit()
        self.db.refresh(account)
        return account