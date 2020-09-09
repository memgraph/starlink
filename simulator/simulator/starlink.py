from simulator.database import Memgraph, connection
from simulator.models import City, Orbit
from simulator import orbital_mechanics_utils
from simulator import db_operations
from skyfield.api import load as skyfield_load
from pathlib import Path
import numpy as np
import time
import os

_here = Path(__file__).parent

ts = skyfield_load.timescale(builtin=True)
minutes = np.arange(0, 24*60*5, 1)
time_of_simulation = ts.utc(2020, 7, 29, 0, minutes)


TLE_FILE_PATH = os.getenv('TLE_FILE_PATH', 'imports/tle_1')
CITIES_FILE_PATH = os.getenv('CITIES_FILE_PATH', 'imports/cities.csv')
DB_UPDATE_TIME = int(os.getenv('DB_UPDATE_TIME', 0))


def run() -> None:

    db = Memgraph()
    db_operations.clear(db)

    tle_path = _here.parent.joinpath(TLE_FILE_PATH)
    ObjectsAndOrbits = orbital_mechanics_utils.generate_orbits_and_moving_objects(
        tle_path, time_of_simulation)

    cities_path = _here.parent.joinpath(CITIES_FILE_PATH)
    cities = City.generate_cities(cities_path, time_of_simulation)

    City.update_cities(cities, ObjectsAndOrbits.moving_objects_dict_by_id)

    Orbit.update_orbits(
        ObjectsAndOrbits.orbits_dict_by_id, ObjectsAndOrbits.moving_objects_dict_by_id)

    db.execute_transaction(connection.WRITE_TRANSACTION, db_operations.create_data,
                           {"moving_objects_dict_by_id": ObjectsAndOrbits.moving_objects_dict_by_id,
                            "cities": cities})

    while(True):
        Orbit.update_orbits(ObjectsAndOrbits.orbits_dict_by_id,
                            ObjectsAndOrbits.moving_objects_dict_by_id)
        City.update_cities(cities, ObjectsAndOrbits.moving_objects_dict_by_id)

        db.execute_transaction(connection.WRITE_TRANSACTION, db_operations.update_data,
                               {"moving_objects_dict_by_id": ObjectsAndOrbits.moving_objects_dict_by_id,
                                "cities": cities})
        time.sleep(DB_UPDATE_TIME)
