from simulator.database import Memgraph
from simulator.models import City
from simulator import utils
from simulator import relation_utils
from simulator import orbital_mechanics_utils
from simulator import db_operations
from simulator.constants import DB_UPDATE_TIME
import time
from skyfield.api import load as skyfield_load
import numpy as np
import os


ts = skyfield_load.timescale(builtin=True)
minutes = np.arange(0, 24*60*5, 1)
time_of_simulation = ts.utc(2020, 7, 29, 0, minutes)


def run():

    db = Memgraph()
    db_operations.clear(db)

    ObjectsAndOrbits = orbital_mechanics_utils.generate_orbits_and_moving_objects(
        os.getenv('TLE_FILE_PATH', 'imports/tle_1'), time_of_simulation)

    cities = City.generate_cities(
        os.getenv('CITIES_FILE_PATH', 'imports/cities.csv'), time_of_simulation)

    relation_utils.update_city_moving_object_distances(
        cities, ObjectsAndOrbits.moving_objects_dict_by_id)

    relation_utils.update_laser_connections(
        ObjectsAndOrbits.orbits_dict_by_id, ObjectsAndOrbits.moving_objects_dict_by_id)

    db.execute_transaction(db_operations.create_data,
                           ObjectsAndOrbits.moving_objects_dict_by_id, cities)

    while(True):
        relation_utils.update_all_positions_and_relations(
            cities, ObjectsAndOrbits.orbits_dict_by_id, ObjectsAndOrbits.moving_objects_dict_by_id)

        db.execute_transaction(db_operations.update_data,
                               ObjectsAndOrbits.moving_objects_dict_by_id, cities)
        time.sleep(DB_UPDATE_TIME)
