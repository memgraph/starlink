import pytest
from starlink_simulator.database import Memgraph, Node
from starlink_simulator import query


@pytest.fixture
def clear_db():
    db = Memgraph()
    db.execute_query('MATCH (n) DETACH DELETE n')


@pytest.mark.parametrize('command, results', [
    ('MATCH (n) RETURN n', []),
    ('MATCH ()-[e]-() RETURN e', []),
    ('MATCH (n) RETURN count(n) as cnt', [{'cnt': 0}])
])
def test_query_on_empty_database(command, results, clear_db):
    actual_results = list(query(command))
    assert actual_results == results


def test_query_create_count(clear_db):
    create_command = '''
    CREATE
        (n: Hello {message: "Hello"}),
        (m: World {message: "World"})
    RETURN n, m;
    '''
    actual_results = list(query(create_command))
    assert len(actual_results) == 1
    assert set(actual_results[0].keys()) == {'n', 'm'}
    for result in actual_results[0].values():
        assert isinstance(result, Node)

    count_command = 'MATCH (n) RETURN count(n) as cnt'
    assert list(query(count_command)) == [{'cnt': 2}]
