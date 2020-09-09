import collections
from typing import Any, Dict, List
from demo.database.memgraph import Memgraph


def import_all_cities(db: Memgraph) -> Dict[str, Any]:
    command = "MATCH (n:City) RETURN n;"
    return db.execute_and_fetch(command)


def import_sats_and_rels(tx: Any, arguments: Dict[str, Any]) -> Dict[str, Any]:
    results = {}

    command = "MATCH (s:Satellite) RETURN s;"
    results["satellites"] = tx.run(command)

    command = "MATCH (s1:Satellite)-[r]-(s2:Satellite) RETURN r, s1, s2;"
    results["relationships"] = tx.run(command)

    return results


def import_data(tx: Any, arguments: Dict[str, Any]) -> Dict[str, Any]:
    results = {}

    command = "MATCH (s:Satellite) RETURN s;"
    results["satellites"] = tx.run(command)

    command = "MATCH p=(c1:City { id: '" + str(arguments["city_one"]) + \
        "'})-[rs *wShortest (e, n | e.transmission_time) total_transmission_time]-(c2:City { id: '" + str(
        arguments["city_two"]) + "'}) WHERE ALL(x IN nodes(p)[1..-1] WHERE (x:Satellite))  RETURN nodes(p), rs;"
    results["shortest_path"] = tx.run(command)

    command = "MATCH (s1:Satellite)-[r]-(s2:Satellite) RETURN r, s1, s2;"
    results["relationships"] = tx.run(command)

    return results
