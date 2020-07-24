from starlink_simulator.database import Memgraph
import starlink_simulator.utils as utils
import starlink_simulator.relation_utils as ru
import starlink_simulator.db_operations as db_operations
import starlink_simulator.constants as const
import time


def starlink(tmp: str) -> str:

    db = Memgraph()
    db_operations.clear(db)

    ru.init_orbits_and_objects(const.NUM_ORB_H, const.NUM_ORB_V,
                               const.NUM_OBJ_ORB, const.SIZE, const.SPEED, const.SAT_ALT)

    cities_csv_path = "starlink_simulator/cities.csv"
    cities = utils.import_cities(cities_csv_path)
    ru.update_city_moving_object_distances(cities, ru.all_moving_objects)

    orbits = (ru.horizontal_orbits + ru.vertical_orbits)
    ru.update_laser_connections(
        orbits, const.NUM_ORB_H, const.NUM_ORB_V, ru.all_moving_objects)

    db_operations.create_moving_objects(db, ru.all_moving_objects)
    db_operations.create_cities(db, cities)
    db_operations.create_city_moving_objects_visibility(
        db, cities, ru.all_moving_objects)
    db_operations.create_laser_connections(db, ru.all_moving_objects)

    while(True):
        ru.update_moving_object_positions(orbits)
        ru.update_laser_connections(
            orbits, const.NUM_ORB_H, const.NUM_ORB_V, ru.all_moving_objects)
        ru.update_city_moving_object_distances(cities, ru.all_moving_objects)

        db_operations.update_object_positions(db, ru.all_moving_objects)
        db_operations.update_city_moving_objects_visibility(
            db, cities, ru.all_moving_objects)
        db_operations.update_laser_connections(db, ru.all_moving_objects)
        #db_operations.establish_connection(db, cities[0], cities[1])

        time.sleep(10)
