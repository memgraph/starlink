from src.database import Memgraph
import src.utils as utils
import src.relation_utils as relation_utils
import src.orbital_mechanics_utils as orbital_mechanics_utils
import src.db_operations as db_operations
import src.constants as const
import time


def starlink(tmp: str) -> str:

    db = Memgraph()
    db_operations.clear(db)

    orbits, orbits_dict, moving_objects, moving_objects_dict = orbital_mechanics_utils.generateMovingObjects()

    cities = orbital_mechanics_utils.import_cities()

    relation_utils.update_city_moving_object_distances(cities, moving_objects)

    relation_utils.update_laser_connections(
        orbits, orbits_dict, moving_objects_dict)

    db.execute_transaction(db_operations.create_data, moving_objects, cities)

    while(True):
        relation_utils.update_all_positions_and_relations(
            cities, orbits, orbits_dict, moving_objects, moving_objects_dict)

        db.execute_transaction(db_operations.update_data,
                               moving_objects, cities)
        time.sleep(const.DB_UPDATE_TIME)
