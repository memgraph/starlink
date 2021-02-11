import csv
import time
import json
import logging
from pathlib import Path
from typing import Any, List
from demo.database import Memgraph
from demo.db_operations import import_all_cities


logger = logging.getLogger('web')


def json_cities(db: Memgraph) -> "JSON":
    start_time = time.time()

    json_cities = {}
    cities = list(import_all_cities(db))
    while len(cities) == 0:
        time.sleep(1)
        cities = list(import_all_cities(db))

    for city in cities:
        c = city['n']
        json_cities[c.properties['id']] = [
            c.properties['x'], c.properties['y'], c.properties['name']]

    logger.info(f'City JSON created in {time.time() - start_time} seconds.')
    return json.dumps(json_cities)


def json_optical_paths(file_path: str) -> "JSON":
    start_time = time.time()

    json_optical_paths = []
    with file_path.open() as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            json_optical_paths.append([
                row["Source"],
                row["Destination"],
                row["Latency"]])

    logger.info(
        f'Optical path JSON created in {time.time() - start_time} seconds.')
    return json.dumps(json_optical_paths)


def json_shortest_path(shortest_path: Any) -> "JSON":
    start_time = time.time()

    json_shortest_path = []
    sp_list = list(shortest_path)
    if(sp_list == []):
        return 0

    sp_relationships = sp_list[0]['rs']

    for r in sp_relationships:
        first_label = 0
        if "City" in r.nodes[0]._labels:
            first_label = 1
        json_shortest_path.append([int(r.nodes[0]['id']),
                                   int(r.nodes[1]['id']),
                                   first_label,
                                   r['transmission_time']])

    logger.info(
        f'Shortest path JSON created in {time.time() - start_time} seconds.')
    return json.dumps(json_shortest_path)
