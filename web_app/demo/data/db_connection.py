import demo.data.db_operations as db_operations
from demo.database import Memgraph
from demo.data.model import City, Satellite, Relationship, OpticalPath
from typing import Any, List


def fetch_cities(db: Memgraph) -> List[City]:
    city_markers = []
    cities = db_operations.import_all_cities(db)
    for cit in cities:
        c = cit['n']
        city_obj = City(
            c.properties['id'], c.properties['x'], c.properties['y'], c.properties['name'])
        city_markers.append(city_obj)
    return city_markers


def transform_satellites(satellites: Any) -> List[Satellite]:
    sat_markers = []
    for sat in satellites:
        s = sat['s']
        sat_obj = Satellite(
            s.properties['id'], s.properties['x'], s.properties['y'], s.properties['z'])
        sat_markers.append(sat_obj)
    return sat_markers


def transform_relationships(relationships: Any) -> List[Relationship]:
    relations = []
    for rel in relationships:
        r = rel['r']
        s1 = rel['s1']
        s2 = rel['s2']
        rel_obj = Relationship(s1.properties['x'], s1.properties['y'], s1.properties['z'],
                               s2.properties['x'], s2.properties['y'], s2.properties['z'],
                               r.properties['transmission_time'])
        relations.append(rel_obj)
    return relations


def transform_shortest_path(shortest_path: Any) -> List[Relationship]:
    shortest_path_list = []
    sp_list = list(shortest_path)
    if(sp_list == []):
        return 0
    sp_relationships = sp_list[0]['rs']
    for r in sp_relationships:
        sp_rel = Relationship(r.nodes[0]['x'], r.nodes[0]['y'], r.nodes[0]['z'],
                              r.nodes[1]['x'], r.nodes[1]['y'], r.nodes[1]['z'],
                              r['transmission_time'])
        shortest_path_list.append(sp_rel)
    return shortest_path_list


def city_json_format(cities: List[City]) -> List[Any]:
    json_cities = []
    for city in cities:
        json_cities.append([city.id, city.x, city.y, city.name])
    return json_cities


def satellite_json_format(satellites: List[Satellite]) -> List[Any]:
    json_satellites = []
    for satellite in satellites:
        json_satellites.append([satellite.x, satellite.y, satellite.z])
    return json_satellites


def relationship_json_format(relationships: List[Relationship]) -> List[Any]:
    json_relationships = []
    for r in relationships:
        json_relationships.append(
            [r.xS, r.yS, r.xE, r.yE, r.transmission_time])
    return json_relationships


def shortest_path_json_format(shortest_path: List[Relationship]) -> List[Any]:
    json_shortest_path = []
    for sp in shortest_path:
        json_shortest_path.append(
            [sp.xS, sp.yS, sp.xE, sp.yE, sp.transmission_time])
    return json_shortest_path


def optical_paths_json_format(optical_paths: List[OpticalPath]) -> List[Any]:
    json_optical_paths = []
    for op in optical_paths:
        json_optical_paths.append(
            [op.city1, op.city2, op.transmission_time_ms])
    return json_optical_paths
