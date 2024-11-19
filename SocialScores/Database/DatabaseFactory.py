from Database.Sqlite3Database import SQLiteDatabase


class DatabaseFactory:
    def create(self, type, db_name):
        if type == 'sqlite':
            return SQLiteDatabase(db_name)
        else:
            return None