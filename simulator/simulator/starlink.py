from simulator.database import Memgraph
from simulator.models import City, Orbit
from simulator import orbital_mechanics_utils
from simulator import db_operations
import time
from skyfield.api import load as skyfield_load
import numpy as np
import os


ts = skyfield_load.timescale(builtin=True)
minutes = np.arange(0, 24*60*5, 1)
time_of_simulation = ts.utc(2020, 7, 29, 0, minutes)


TLE_FILE_PATH = os.getenv('TLE_FILE_PATH', 'imports/tle_1')
CITIES_FILE_PATH = os.getenv('CITIES_FILE_PATH', 'imports/cities.csv')
DB_UPDATE_TIME = int(os.getenv('DB_UPDATE_TIME', 0))


def run() -> None:

    db = Memgraph()
    db_operations.clear(db)

    ObjectsAndOrbits = orbital_mechanics_utils.generate_orbits_and_moving_objects(
        TLE_FILE_PATH, time_of_simulation)

    cities = City.generate_cities(CITIES_FILE_PATH, time_of_simulation)

    City.update_cities(cities, ObjectsAndOrbits.moving_objects_dict_by_id)

    Orbit.update_orbits(
        ObjectsAndOrbits.orbits_dict_by_id, ObjectsAndOrbits.moving_objects_dict_by_id)

    db.execute_transaction(db_operations.create_data,
                           ObjectsAndOrbits.moving_objects_dict_by_id, cities)

    while(True):
        Orbit.update_orbits(ObjectsAndOrbits.orbits_dict_by_id,
                            ObjectsAndOrbits.moving_objects_dict_by_id)
        City.update_cities(cities, ObjectsAndOrbits.moving_objects_dict_by_id)

        db.execute_transaction(db_operations.update_data,
                               ObjectsAndOrbits.moving_objects_dict_by_id, cities)
        time.sleep(DB_UPDATE_TIME)
