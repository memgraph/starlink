from demo.database import Memgraph
import demo.data.db_operations as db_operations
from demo.data.model import City, Satellite, Relationship, OpticalPath


def fetch_cities(db):
    city_markers = []
    cities = db_operations.import_all_cities(db)
    for cit in cities:
        c = cit['n']
        city_obj = City(
            c.properties['id'], c.properties['x'], c.properties['y'], c.properties['name'])
        city_markers.append(city_obj)
    return city_markers


def fetch_satellites(db):
    satellites = db_operations.import_initial_satellites(db)
    return transform_satellites(satellites)


def fetch_relationships(db):
    relationships = db_operations.import_initial_relationships(db)
    return transform_relationships(relationships)


def transform_satellites(satellites):
    sat_markers = []
    for sat in satellites:
        s = sat['s']
        sat_obj = Satellite(
            s.properties['id'], s.properties['x'], s.properties['y'], s.properties['z'])
        sat_markers.append(sat_obj)
    return sat_markers


def transform_relationships(relationships):
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


def transform_shortest_path(shortest_path_info):
    shortest_path = []
    sp_list = list(shortest_path_info)
    if(sp_list == []):
        return 0
    sp_relationships = sp_list[0]['rs']
    for r in sp_relationships:
        sp_rel = Relationship(r.nodes[0]['x'], r.nodes[0]['y'], r.nodes[0]['z'], 
                              r.nodes[1]['x'], r.nodes[1]['y'], r.nodes[1]['z'], 
                              r['transmission_time'])
        shortest_path.append(sp_rel)
    return shortest_path


def city_json_format(cities):
    json_cities = []
    for city in cities:
        json_cities.append([city.id, city.x, city.y, city.name])
    return json_cities


def satellite_json_format(satellites):
    json_satellites = []
    for satellite in satellites:
        json_satellites.append([satellite.x, satellite.y, satellite.z])
    return json_satellites


def relationship_json_format(relationships):
    json_relationships = []
    for r in relationships:
        json_relationships.append(
            [r.xS, r.yS, r.xE, r.yE, r.transmission_time])
    return json_relationships


def shortest_path_json_format(shortest_path):
    json_shortest_path = []
    for sp in shortest_path:
        json_shortest_path.append(
            [sp.xS, sp.yS, sp.xE, sp.yE, sp.transmission_time])
    return json_shortest_path


def optical_paths_json_format(optical_paths):
    json_optical_paths = []
    for op in optical_paths:
        json_optical_paths.append(
            [op.city1, op.city2, op.transmission_time_ms])
    return json_optical_paths