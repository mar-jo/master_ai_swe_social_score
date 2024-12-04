import psycopg2
from typing import List, Dict, Tuple
from SocialScores.Database.DatabaseBase import Database

class PostgreSQLDatabase(Database):
    def __init__(self, db_name: str, user: str, password: str, host: str = 'localhost', port: int = 5432):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self) -> None:
        """Establish a connection to the PostgreSQL database."""
        self.connection = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        """Close the connection to the PostgreSQL database."""
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def execute(self, query: str, params: Tuple = ()) -> None:
        """Execute a single query (insert, update, delete)."""
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetchall(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """Fetch all rows for a given query."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query: str, params: Tuple = ()) -> Tuple:
        """Fetch a single row for a given query."""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        """Create a table with the provided columns."""
        columns_def = ", ".join(f"{name} {dtype}" for name, dtype in columns.items())
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
        self.execute(query)

    def insert(self, table: str, data: Dict[str, any]) -> None:
        """Insert a row into the table."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(f"%s" for _ in data)
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.execute(query, tuple(data.values()))

    def update(self, table: str, data: Dict[str, any], where: str, where_params: Tuple) -> None:
        """Update rows in the table."""
        set_clause = ", ".join(f"{key} = %s" for key in data)
        query = f"UPDATE {table} SET {set_clause} WHERE {where}"
        self.execute(query, tuple(data.values()) + where_params)

    def delete(self, table: str, where: str, where_params: Tuple) -> None:
        """Delete rows from the table."""
        query = f"DELETE FROM {table} WHERE {where}"
        self.execute(query, where_params)