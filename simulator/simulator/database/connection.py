from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator
from simulator.database.models import Node, Relationship
from neo4j import GraphDatabase, basic_auth, unit_of_work
from neo4j.types import Relationship as Neo4jRelationship
from neo4j.types import Node as Neo4jNode


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
    def create(**kwargs) -> 'Connection':
        return Neo4jConnection(**kwargs)


class Neo4jConnection(Connection):
    def __init__(self,
                 host: str,
                 port: int,
                 username: str,
                 password: str,
                 encrypted: bool):
        super().__init__(host, port, username, password, encrypted)
        self._connection = self._create_connection()

    def execute_query(self, query: str) -> None:
        """Executes Cypher query without returning any results."""
        with self._connection.session() as session:
            session.run(query)

    def execute_and_fetch(self, query: str) -> Iterator[Dict[str, Any]]:
        """Executes Cypher query and returns iterator of results."""
        with self._connection.session() as session:
            results = session.run(query)
            columns = results.keys()
            for result in results:
                yield {
                    column: _convert_neo4j_value(result[column])
                    for column in columns}

    def execute_transaction(self,
                            transaction_type: int,
                            func: Any,
                            arguments: Dict[str, Any]) -> Any:
        """Executes Cypher queries as one transaction and returns dictionary of results."""
        with self._connection.session() as session:
            if(transaction_type == READ_TRANSACTION):
                transaction_results = session.read_transaction(func, arguments)
            else:
                transaction_results = session.write_transaction(func, arguments)
        print("111")
        output = {}
        for key in transaction_results.keys():
            output[key] = []
            columns = transaction_results[key].keys()
            for result in transaction_results[key]:
                output[key].append({
                    column: _convert_neo4j_value(result[column])
                    for column in columns})
        print("222")
        return output
    
    def is_active(self) -> bool:
        """Returns True if connection is active and can be used"""
        return self._connection is not None

    def _create_connection(self):
        return GraphDatabase.driver(
            f'bolt://{self.host}:{self.port}',
            auth=basic_auth(self.username, self.password),
            encrypted=self.encrypted)


def _convert_neo4j_value(value: Any) -> Any:
    """Converts Neo4j objects to custom Node/Relationship objects"""
    if isinstance(value, Neo4jRelationship):
        return Relationship(
            rel_id=value.id,
            rel_type=value.type,
            start_node=value.start_node,
            end_node=value.end_node,
            properties=dict(value.items()))

    if isinstance(value, Neo4jNode):
        return Node(
            node_id=value.id,
            labels=value.labels,
            properties=dict(value.items()))

    return value
