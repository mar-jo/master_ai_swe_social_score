from abc import ABC, abstractmethod
from typing import List, Dict, Tuple

class Database(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Establish a connection to the database."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the connection to the database."""
        pass

    @abstractmethod
    def execute(self, query: str, params: Tuple = ()) -> None:
        """Execute a single query (insert, update, delete)."""
        pass

    @abstractmethod
    def fetchall(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """Fetch all rows for a given query."""
        pass

    @abstractmethod
    def fetchone(self, query: str, params: Tuple = ()) -> Tuple:
        """Fetch a single row for a given query."""
        pass

    @abstractmethod
    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        """Create a table with the provided columns."""
        pass

    @abstractmethod
    def insert(self, table: str, data: Dict[str, any]) -> None:
        """Insert a row into the table."""
        pass

    @abstractmethod
    def update(self, table: str, data: Dict[str, any], where: str, where_params: Tuple) -> None:
        """Update rows in the table."""
        pass

    @abstractmethod
    def delete(self, table: str, where: str, where_params: Tuple) -> None:
        """Delete rows from the table."""
        pass
