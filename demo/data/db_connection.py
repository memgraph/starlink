from demo.database import Memgraph
import demo.data.db_operations as db_operations

import demo.data.satellite as S
import demo.data.city as C


sat_markers = []
city_markers = []

def fetch_cities(db):
    cities = db_operations.import_all_cities(db)
    for cit in cities:
        c = cit['n']
        city_obj = C.City(c.properties['id'], c.properties['x'], c.properties['y'], c.properties['name'])
        sat_markers.append(city_obj)
    return sat_markers

def fetch_satellites(db):
    satellites = db_operations.import_all_satellites(db)
    for sat in satellites:
        s = sat['n']
        sat_obj = S.Satellite(s.properties['id'], s.properties['x'], s.properties['y'], s.properties['z'])
        sat_markers.append(sat_obj)
    return sat_markers

