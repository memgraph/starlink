from starlink_simulator.database import Memgraph
import starlink_simulator.utils as utils
import starlink_simulator.relation_utils as relation_utils
import starlink_simulator.orbital_mechanics_utils as orbital_mechanics_utils
import starlink_simulator.db_operations as db_operations
import starlink_simulator.constants as const
import time


def starlink(tmp: str) -> str:

    db = Memgraph()

    orbits, orbits_dict, moving_objects, moving_objects_dict = orbital_mechanics_utils.generateMovingObjects()

    cities = orbital_mechanics_utils.import_cities()

    relation_utils.update_city_moving_object_distances(cities, moving_objects)
    relation_utils.update_laser_connections(
        orbits, orbits_dict, moving_objects_dict)

    db.execute_transaction(db_operations.create_data, moving_objects, cities)

    while(True):
        relation_utils.update_all_positions_and_relations(
            cities, orbits, orbits_dict, moving_objects, moving_objects_dict)
        
        #print(f"{utils.bcolors.WARNING}Simulator DB update START{utils.bcolors.ENDC}")
        
        #db_operations.update_object_positions(db, moving_objects)
        #db_operations.update_city_moving_objects_visibility(db, cities)
        #db_operations.update_laser_connections(db, moving_objects)
        #db_operations.establish_connection(db, cities[0], cities[1])

        db.execute_transaction(db_operations.update_data, moving_objects, cities)
        
        #print(f"{utils.bcolors.WARNING}Simulator DB update END{utils.bcolors.ENDC}")
        
        time.sleep(const.DB_UPDATE_TIME)

