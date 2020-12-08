import time
import logging
import demo.data.db_operations as db_operations
from demo.database import Memgraph
from demo.data.model import City, Satellite, Relationship, OpticalPath
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


def transform_satellites(satellites: Any) -> List[Satellite]:
    start_time = time.time()

    sat_markers = []
    for sat in satellites:
        s = sat['s']
        sat_obj = Satellite(
            s.properties['id'], s.properties['x'], s.properties['y'], s.properties['z'])
        sat_markers.append(sat_obj)

    logger.info(f'Satellite objects created in {time.time() - start_time} seconds.')
    return sat_markers


def transform_relationships(relationships: Any) -> List[Relationship]:
    start_time = time.time()

    relations = []
    for rel in relationships:
        r = rel['r']
        s1 = rel['s1']
        s2 = rel['s2']
        rel_obj = Relationship(s1.properties['x'], s1.properties['y'],
                               s2.properties['x'], s2.properties['y'],
                               r.properties['transmission_time'])
        relations.append(rel_obj)

    logger.info(f'Relationship objects created in {time.time() - start_time} seconds.')
    return relations


def transform_shortest_path(shortest_path: Any) -> List[Relationship]:
    start_time = time.time()

    shortest_path_list = []
    sp_list = list(shortest_path)
    if(sp_list == []):
        return 0

    sp_relationships = sp_list[0]['rs']
    sp_nodes = sp_list[0]['nodes(p)']

    for i in range(0, len(sp_nodes)-1):
        sp_rel = Relationship(sp_nodes[i].properties['x'], sp_nodes[i].properties['y'],
                              sp_nodes[i+1].properties['x'], sp_nodes[i+1].properties['y'],
                              sp_relationships[i].properties['transmission_time'])
        shortest_path_list.append(sp_rel)

    logger.info(f'Shortest path relationship objects created in {time.time() - start_time} seconds.')
    return shortest_path_list


def city_json_format(cities: List[City]) -> List[Any]:
    start_time = time.time()

    json_cities = []
    for city in cities:
        json_cities.append([city.id, city.x, city.y, city.name])

    logger.info(f'Cities JSON created in {time.time() - start_time} seconds.')
    return json_cities


def satellite_json_format(satellites: List[Satellite]) -> List[Any]:
    start_time = time.time()

    json_satellites = []
    for satellite in satellites:
        json_satellites.append([satellite.x, satellite.y, satellite.z])

    logger.info(f'Satellites JSON created in {time.time() - start_time} seconds.')
    return json_satellites


def relationship_json_format(relationships: List[Relationship]) -> List[Any]:
    start_time = time.time()

    json_relationships = []
    for r in relationships:
        json_relationships.append(
            [r.xS, r.yS, r.xE, r.yE, r.transmission_time])

    logger.info(f'Relationships JSON created in {time.time() - start_time} seconds.')
    return json_relationships


def shortest_path_json_format(shortest_path: List[Relationship]) -> List[Any]:
    start_time = time.time()

    json_shortest_path = []
    for sp in shortest_path:
        json_shortest_path.append(
            [sp.xS, sp.yS, sp.xE, sp.yE, sp.transmission_time])

    logger.info(f'Shortest path JSON created in {time.time() - start_time} seconds.')
    return json_shortest_path


def optical_paths_json_format(optical_paths: List[OpticalPath]) -> List[Any]:
    start_time = time.time()

    json_optical_paths = []
    for op in optical_paths:
        json_optical_paths.append(
            [op.city1, op.city2, op.transmission_time_ms])

    logger.info(f'Optical path JSON created in {time.time() - start_time} seconds.')
    return json_optical_paths
