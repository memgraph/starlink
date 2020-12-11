import logging
import collections
from typing import Any, Dict, List, Iterator
from database.memgraph import Memgraph
from database.connection import _convert_memgraph_value 


logger = logging.getLogger('data')

 
def import_rels(cursor: Any, arguments: Dict[str, Any]) -> Dict[str, Any]:
    results = {}

    execute_transaction_query(cursor, "BEGIN")

    command = "MATCH (s1:Satellite)-[r]-(s2:Satellite) RETURN r, s1, s2;"
    results["relationships"] = execute_transaction_query_and_fetch(cursor, command)

    execute_transaction_query(cursor, "COMMIT")
    return results


def execute_transaction_query(cursor: Any, query: str) -> None:
    try:
        cursor.execute(query)
        cursor.fetchall()
    except:
        logger.exception(f'Something went wrong with the transaction read query')


def execute_transaction_query_and_fetch(cursor: Any, query: str) -> Iterator[Dict[str, Any]]:
        output = []
        try:
            cursor.execute(query)
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                output.append({
                            dsc.name: _convert_memgraph_value(row[index])
                            for index, dsc in enumerate(cursor.description)})
        except:
            logger.exception(f'Something went wrong with the transaction write query')
        return output
