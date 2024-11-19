import Models.account as Account
import Database as Database

def convert_account_to_dict(account: Account) -> dict:
    return {
        'username': account.username
    }

table_name = 'accounts'

class RepositoryAccount:
    def __init__(self, database: Database):
        self.database = database

    def add_account(self, account : Account):
        self.database.insert(table_name, convert_account_to_dict(account))

    def get_account(self, username):
        return self.database.fetchone(f"SELECT * FROM {table_name} WHERE username = ?", (username,))

    def get_all_accounts(self):
        return self.database.fetchall(f"SELECT * FROM {table_name}")

    #def update_account(self, account):
    #    self.database.update_account(account)

    def delete_account(self, username):
        self.database.delete(table_name, "username = ?", (username,))

