import psycopg2
from psycopg2 import sql
from typing import List, Dict, Tuple
from contextlib import contextmanager

from Database.DatabaseBase import Database

class PostgresDatabase(Database):
    def __init__(self, connection_string: str):
        """
        Initialize the PostgresDatabase with a Data Source Name (DSN).
        DSN should include user, password, host, port, and database.
        dsn = "dbname=testdb user=postgres password=securepassword host=localhost port=5432"
        """
        self.connection_string = connection_string
        self.connection = None

    def connect(self) -> None:
        """Establish a connection to the database."""
        # Split the connection string into key-value pairs
        params = dict(item.split('=') for item in self.connection_string.split())

        print(params)
        try:
            self.connection = psycopg2.connect(
                dbname=params["dbname"],
                user=params["user"],
                password=params["password"],
                host=params["host"],
                port=params["port"],
                options="-c client_encoding=UTF8"
            )
            print("Connected successfully!")
        except Exception as e:
            print("Error:", e)
            raise e

    def close(self) -> None:
        """Close the connection to the database."""
        if self.connection:
            self.connection.close()
            self.connection = None

    @contextmanager
    def cursor(self):
        """Provide a cursor for executing queries."""
        if not self.connection:
            raise Exception("Database connection is not established. Call connect() first.")
        cur = self.connection.cursor()
        try:
            yield cur
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            cur.close()

    def execute(self, query: str, params: Tuple = ()) -> None:
        """Execute a single query."""
        with self.cursor() as cur:
            cur.execute(query, params)

    def fetchall(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """Fetch all rows for a given query."""
        with self.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

    def fetchone(self, query: str, params: Tuple = ()) -> Tuple:
        """Fetch a single row for a given query."""
        with self.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()

    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        """Create a table with the provided columns."""
        with self.cursor() as cur:
            columns_def = ", ".join(f"{col} {datatype}" for col, datatype in columns.items())
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def});"
            cur.execute(query)

    def insert(self, table: str, data: Dict[str, any]) -> None:
        """Insert a row into the table."""
        with self.cursor() as cur:
            columns = data.keys()
            placeholders = ", ".join(["%s"] * len(columns))
            query = sql.SQL(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})")
            cur.execute(query, tuple(data.values()))

    def update(self, table: str, data: Dict[str, any], where: str, where_params: Tuple) -> None:
        """Update rows in the table."""
        with self.cursor() as cur:
            set_clause = ", ".join(f"{key} = %s" for key in data.keys())
            query = sql.SQL(f"UPDATE {table} SET {set_clause} WHERE {where}")
            cur.execute(query, tuple(data.values()) + where_params)

    def delete(self, table: str, where: str, where_params: Tuple) -> None:
        """Delete rows from the table."""
        with self.cursor() as cur:
            query = sql.SQL(f"DELETE FROM {table} WHERE {where}")
            cur.execute(query, where_params)
