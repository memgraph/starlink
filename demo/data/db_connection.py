from demo.database import Memgraph
import demo.data.db_operations as db_operations

import demo.data.satellite as S
import demo.data.city as C


def fetch_cities(db):
    city_markers = []
    cities = db_operations.import_all_cities(db)
    for cit in cities:
        c = cit['n']
        city_obj = C.City(
            c.properties['id'], c.properties['x'], c.properties['y'], c.properties['name'])
        city_markers.append(city_obj)
    return city_markers


def fetch_satellites(db):
    sat_markers = []

    satellites = db_operations.import_all_satellites(db)
    for sat in satellites:
        s = sat['n']
        sat_obj = S.Satellite(
            s.properties['id'], s.properties['x'], s.properties['y'], s.properties['z'])
        sat_markers.append(sat_obj)
    return sat_markers


def city_json_format(cities):
    json_cities = []
    for city in cities:
        json_cities.append([city.x, city.y, city.name])
    return json_cities


def satellite_json_format(satellites):
    json_satellites = []
    for satellite in satellites:
        json_satellites.append([satellite.y, satellite.x, satellite.z])
    return json_satellites
