from Database.DatabaseFactory import DatabaseFactory
from Database.RepositoryAccount import RepositoryAccount, table_name as account_table_name
from Models.account import Account


def hello_world():
    return "Hello, World!"

print(hello_world())

import Database.DatabaseFactory

database_type = 'sqlite'
database_factory = DatabaseFactory()
database = database_factory.create(database_type, 'Database/test.db') # returns an instance of SQLiteDatabase
database.connect()
database.create_table(account_table_name, {'username': 'TEXT'})

testAccount = Account('test')
RepositoryAccount(database).add_account(testAccount)
print('succesfully added account')

readAccount = RepositoryAccount(database).get_account('test')
print('found account with username: ' + readAccount[0])
