from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator
from database.models import Node, Relationship
import mgclient

__all__ = ("Connection",)


READ_TRANSACTION = 0
WRITE_TRANSACTION = 1


class Connection(ABC):
    def __init__(self,
                 host: str,
                 port: int,
                 username: str,
                 password: str,
                 encrypted: bool):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.encrypted = encrypted

    @abstractmethod
    def execute_query(self, query: str) -> None:
        """Executes Cypher query without returning any results."""
        pass

    @abstractmethod
    def execute_and_fetch(self, query: str) -> Iterator[Dict[str, Any]]:
        """Executes Cypher query and returns iterator of results."""
        pass

    @abstractmethod
    def is_active(self) -> bool:
        """Returns True if connection is active and can be used"""
        pass

    @staticmethod
    def create(**kwargs) -> "Connection":
        return MemgraphConnection(**kwargs)

class MemgraphConnection(Connection):
    def __init__(self, host: str, port: int, username: str, password: str, encrypted: bool, lazy: bool = True):
        super().__init__(host, port, username, password, encrypted)
        self.lazy = lazy
        self._connection = self._create_connection()

    def execute_query(self, query: str) -> None:
        """Executes Cypher query without returning any results."""
        cursor = self._connection.cursor()
        cursor.execute(query)
        cursor.fetchall()

    def execute_and_fetch(self, query: str) -> Iterator[Dict[str, Any]]:
        """Executes Cypher query and returns iterator of results."""
        cursor = self._connection.cursor()
        cursor.execute(query)
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield {dsc.name: _convert_memgraph_value(row[index]) for index, dsc in enumerate(cursor.description)}

    def execute_transaction(self,
                            func: Any,
                            arguments: Dict[str, Any]) -> Any:
        """Executes Cypher queries as one transaction and returns dictionary of results."""
        cursor = self._connection.cursor()
        return func(cursor, arguments)
            
    def is_active(self) -> bool:
        """Returns True if connection is active and can be used"""
        return self._connection is not None and self._connection.status == mgclient.CONN_STATUS_READY

    def _create_connection(self):
        sslmode = mgclient.MG_SSLMODE_REQUIRE if self.encrypted else mgclient.MG_SSLMODE_DISABLE
        return mgclient.connect(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            sslmode=sslmode,
            lazy=self.lazy,
        )


def _convert_memgraph_value(value: Any) -> Any:
    """Converts Memgraph objects to custom Node/Relationship objects"""
    if isinstance(value, mgclient.Relationship):
        return Relationship(
            rel_id=value.id,
            rel_type=value.type,
            start_node=value.start_id,
            end_node=value.end_id,
            properties=value.properties,
        )

    if isinstance(value, mgclient.Node):
        return Node(node_id=value.id, labels=value.labels, properties=value.properties)

    return value