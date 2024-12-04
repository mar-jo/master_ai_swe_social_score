from Database.Sqlite3Database import SQLiteDatabase
from Database.PostgreDatabase import PostgresDatabase


class DatabaseFactory:
    def create(self, type, connectionstring):
        if type == 'sqlite':
            return SQLiteDatabase(connectionstring) #connectionstring is the db file name
        elif type == 'postgres':
            # return PostgresDatabase(db_name)
            return PostgresDatabase(connectionstring)
        else:
            return None