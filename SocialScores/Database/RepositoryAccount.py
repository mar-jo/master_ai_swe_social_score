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

    def add_account(self, account_data: dict):
        """
        Add an account directly from a dictionary (for test data initialization).
        """
        hashed_password = bcrypt.hash(account_data["password"])
        new_account = Account(
            email=account_data["email"],
            username=account_data["username"],
            password=hashed_password,
        )
        self.db.add(new_account)
        self.db.commit()
        self.db.refresh(new_account)
        return new_account

    def create_account(self, email: str, username: str, password: str):
        """
        Create an account with validation checks.
        """
        # Check if the email or username is already taken
        if self.db.query(Account).filter_by(email=email).first():
            raise ValueError("Email already registered")
        if self.db.query(Account).filter_by(username=username).first():
            raise ValueError("Username already taken")

        # Hash the password and create a new account
        hashed_password = bcrypt.hash(password)
        new_account = Account(email=email, username=username, password=hashed_password)
        self.db.add(new_account)
        self.db.commit()
        self.db.refresh(new_account)
        return new_account

    def get_account_by_email(self, email: str):
        return self.db.query(Account).filter_by(email=email).first()

    def get_account_by_username(self, username: str):
        return self.db.query(Account).filter_by(username=username).first()

    def validate_login(self, username: str, password: str):
        """
        Validate login credentials.
        """
        account = self.db.query(Account).filter_by(username=username).first()
        if account and bcrypt.verify(password, account.password):  # Verify hashed password
            return account
        raise ValueError("Invalid username or password")
