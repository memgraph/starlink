import collections
from typing import Any, Dict, List, Iterator
from demo.database.memgraph import Memgraph
from demo.database.connection import _convert_memgraph_value 


def import_all_cities(db: Memgraph) -> Dict[str, Any]:
    command = "MATCH (n:City) RETURN n;"
    return db.execute_and_fetch(command)


def import_sats_and_rels(cursor: Any, arguments: Dict[str, Any]) -> Dict[str, Any]:
    results = {}

    command = "MATCH (s:Satellite) RETURN s;"
    results["satellites"] = execute_transaction_query_and_fetch(cursor, command)


    command = "MATCH (s1:Satellite)-[r]-(s2:Satellite) RETURN r, s1, s2;"
    results["relationships"] = execute_transaction_query_and_fetch(cursor, command)

    return results


def import_data(cursor: Any, arguments: Dict[str, Any]) -> Dict[str, Any]:
    results = {}

    command = "MATCH (s:Satellite) RETURN s;"
    results["satellites"] = execute_transaction_query_and_fetch(cursor, command)

    command = "MATCH p=(c1:City { id: '" + str(arguments["city_one"]) + \
        "'})-[rs *wShortest (e, n | e.transmission_time) total_transmission_time]-(c2:City { id: '" + str(
        arguments["city_two"]) + "'}) WHERE ALL(x IN nodes(p)[1..-1] WHERE (x:Satellite))  RETURN p, nodes(p), rs;"
    results["shortest_path"] = execute_transaction_query_and_fetch(cursor, command)

    command = "MATCH (s1:Satellite)-[r]-(s2:Satellite) RETURN r, s1, s2;"
    results["relationships"] = execute_transaction_query_and_fetch(cursor, command)

    return results


def execute_transaction_query_and_fetch(cursor: Any, query: str) -> Iterator[Dict[str, Any]]:
        cursor.execute(query)
        output = []
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            output.append({
                        dsc.name: _convert_memgraph_value(row[index])
                        for index, dsc in enumerate(cursor.description)})
        return output
