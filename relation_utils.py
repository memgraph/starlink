import utils


# Updates the position of each object in all orbits
def update_moving_object_positions(orbits):
    for orbit in orbits:
        orbit.update_moving_object_positions()


def update_city_positions(cities):
    for city in cities:
        city.update_position()


# Updates all distances between all cities and all moving objects
def update_city_moving_object_distances(cities, moving_objects):
    for city in cities:
        city.city_visible_moving_object_distances(moving_objects)


# Updates all object laser connections
def update_laser_connections(orbits, orbits_dict, moving_objects_dict):
    for orbit in orbits:
        orbit.update_laser_connections(orbits_dict)
        orbit.update_laser_distances(moving_objects_dict)


def update_all_positions_and_relations(cities, orbits, orbits_dict, moving_objects, moving_objects_dict):
    update_moving_object_positions(orbits)
    update_city_positions(cities)
    update_city_moving_object_distances(cities, moving_objects)
    update_laser_connections(orbits, orbits_dict, moving_objects_dict)
