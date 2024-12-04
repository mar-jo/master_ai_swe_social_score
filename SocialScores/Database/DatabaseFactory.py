from SocialScores.Database.Sqlite3Database import SQLiteDatabase
from SocialScores.Database.PostgreSQLDatabase import PostgreSQLDatabase

class DatabaseFactory:
    def create(self, type: str, db_name: str, **kwargs):
        if type == 'sqlite':
            return SQLiteDatabase(db_name)
        elif type == 'postgresql':
            user = kwargs.get('user')
            password = kwargs.get('password')
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', 5432)

            # Validate mandatory fields
            if not user or not password:
                raise ValueError("Missing required credentials for PostgreSQL: 'user' and 'password'")

            return PostgreSQLDatabase(
                db_name=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
        else:
            raise ValueError(f"Unsupported database type: {type}")
