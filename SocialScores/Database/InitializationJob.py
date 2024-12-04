from Database.DatabaseFactory import DatabaseFactory
from Database.RepositoryAccount import RepositoryAccount, table_name as account_table_name, columns as account_columns
from Models.account import Account

database_engine = 'postgres'
connection_string = 'dbname=socialscores user=postgres password=Test1234 host=localhost port=5432'

def start():
    db_factory = DatabaseFactory()
    database = db_factory.create(database_engine, connection_string)

    database.connect()

    drop_all(database)
    create_all(database)
    populate(database)

def drop_all(database):
    database.execute(f"DROP TABLE IF EXISTS {account_table_name}")

def create_all(database):
    database.create_table(account_table_name, account_columns)

def populate(database):
    testAccount = Account('test')
    RepositoryAccount(database).add_account(testAccount)
    print('succesfully added account')

    readAccount = RepositoryAccount(database).get_account('test')
    print('found account with username: ' + readAccount[0])
