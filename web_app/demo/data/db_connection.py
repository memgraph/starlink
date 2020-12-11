import time
import json
import logging
import demo.data.db_operations as db_operations
from demo.database import Memgraph
from demo.data.model import City, OpticalPath
from typing import Any, List


logger = logging.getLogger('web')


def fetch_cities(db: Memgraph) -> List[City]:
    start_time = time.time()

    city_markers = []
    cities = db_operations.import_all_cities(db)
    for cit in cities:
        c = cit['n']
        city_obj = City(
            c.properties['id'], c.properties['x'], c.properties['y'], c.properties['name'])
        city_markers.append(city_obj)

    logger.info(f'City objects created in {time.time() - start_time} seconds.')
    return city_markers


def city_json_format(cities: List[City]) -> List[Any]:
    start_time = time.time()

    json_cities = []
    for city in cities:
        json_cities.append([city.id, city.x, city.y, city.name])

    logger.info(f'Cities JSON created in {time.time() - start_time} seconds.')
    return json_cities


def optical_paths_json_format(optical_paths: List[OpticalPath]) -> List[Any]:
    start_time = time.time()

    json_optical_paths = []
    for op in optical_paths:
        json_optical_paths.append(
            [op.city1, op.city2, op.transmission_time_ms])

    logger.info(
        f'Optical path JSON created in {time.time() - start_time} seconds.')
    return json_optical_paths


def json_relationships_satellites(relationships: Any) -> Any:
    start_time = time.time()

    json_relationships = []
    json_satellites = []
    sat_ids = set()
    for rel in relationships:
        r = rel['r']
        s1 = rel['s1']
        s2 = rel['s2']

        json_relationships.append([s1.properties['x'], s1.properties['y'],
                                   s2.properties['x'], s2.properties['y'], r.properties['transmission_time']])

        if(not s1.properties['id'] in sat_ids):
            json_satellites.append([int(s1.properties['id']), s1.properties['x'], s1.properties['y']])
            sat_ids.add(s1.properties['id'])
        if(not s2.properties['id'] in sat_ids):
            json_satellites.append([int(s2.properties['id']), s2.properties['x'], s2.properties['y']])
            sat_ids.add(s2.properties['id'])

    logger.info(
        f'Relationship and Satellite JSON created in {time.time() - start_time} seconds.')
    return json.dumps(json_relationships), json.dumps(json_satellites)


def json_shortest_path(shortest_path: Any) -> List[str]:
    start_time = time.time()

    json_shortest_path = []
    sp_list = list(shortest_path)
    if(sp_list == []):
        return 0

    sp_relationships = sp_list[0]['rs']
    sp_nodes = sp_list[0]['nodes(p)']

    for i in range(0, len(sp_nodes)-1):
        json_shortest_path.append([int(sp_nodes[i].properties['id']),
                                   int(sp_nodes[i+1].properties['id']),
                                   sp_relationships[i].properties['transmission_time']])

    logger.info(
        f'Shortest path JSON created in {time.time() - start_time} seconds.')
    return json.dumps(json_shortest_path)
