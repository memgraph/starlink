

def update_moving_object_positions(orbits_dict_by_id):
    for orbit_id in orbits_dict_by_id.keys():
        orbits_dict_by_id[orbit_id].update_moving_object_positions()


def update_city_positions(cities):
    for city in cities:
        city.update_position()


def update_city_moving_object_distances(cities, moving_objects_dict_by_id):
    for city in cities:
        city.city_visible_moving_object_distances(moving_objects_dict_by_id)


def update_laser_connections(orbits_dict_by_id, moving_objects_dict_by_id):
    for orbit_id in orbits_dict_by_id.keys():
        orbits_dict_by_id[orbit_id].update_laser_connections(orbits_dict_by_id)
        orbits_dict_by_id[orbit_id].update_laser_distances(
            moving_objects_dict_by_id)


def update_all_positions_and_relations(cities, orbits_dict_by_id, moving_objects_dict_by_id):
    update_moving_object_positions(orbits_dict_by_id)
    update_city_positions(cities)
    update_city_moving_object_distances(cities, moving_objects_dict_by_id)
    update_laser_connections(orbits_dict_by_id, moving_objects_dict_by_id)
