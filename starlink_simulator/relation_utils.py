from starlink_simulator.utils import distance3D as d3D
from starlink_simulator.orbit import Orbit
from starlink_simulator.moving_object import MovingObject as MO
from starlink_simulator.constants import VIEW_ANGLE


horizontal_orbits = []
horizontal_orbits_dict = {}

vertical_orbits = []
vertical_orbits_dict = {}

all_moving_objects = []
all_moving_objects_dict = {}


# Initializes orbits and their objects
def init_orbits_and_objects(num_of_orbits_horizontal, num_of_orbits_vertical, num_of_objects_in_orbit_h, num_of_objects_in_orbit_v, size_x, size_y, moving_object_speed, satellite_altitude):
    orbit_id = 0
    moving_object_id = 0

    # Creates horizontal orbits and their objects
    for x in range(num_of_orbits_horizontal):
        orbit = Orbit(id=orbit_id, id_in_orbit_group=x, is_horizontal=True, x_start=-size_x/2.0, y_start=(x+1.0)*(size_y/(num_of_orbits_horizontal+1.0))-90.0, x_end=size_x/2.0-1.0, y_end=(x+1.0)*(size_y/(num_of_orbits_horizontal+1.0))-90.0,
                      number_of_objects=num_of_objects_in_orbit_h, moving_object_speed=moving_object_speed)
        for y in range(num_of_objects_in_orbit_h):
            if y == 0:
                laser_left_id = num_of_objects_in_orbit_h + \
                    (num_of_objects_in_orbit_h * (x+1)) - 1
                laser_left_id_in_orbit = num_of_objects_in_orbit_h - 1
                laser_right_id = moving_object_id + 1
                laser_right_id_in_orbit = y+1
            elif y == num_of_objects_in_orbit_h - 1:
                laser_left_id = moving_object_id - 1
                laser_left_id_in_orbit = y-1
                laser_right_id = num_of_objects_in_orbit_h * (x+1)
                laser_right_id_in_orbit = 0
            else:
                laser_left_id = moving_object_id - 1
                laser_left_id_in_orbit = y-1
                laser_right_id = moving_object_id + 1
                laser_right_id_in_orbit = y+1

            mo = MO(id=moving_object_id, id_in_orbit=y, orbit_id=orbit_id, is_in_horizontal_orbit=True, x0=y*(size_x*1.0/num_of_objects_in_orbit_h)-180.0,
                    y0=(x+1.0)*(size_y/(num_of_orbits_horizontal+1.0))-90.0, z0=satellite_altitude, laser_left_id=laser_left_id, laser_left_id_in_orbit=laser_left_id_in_orbit, laser_right_id=laser_right_id, laser_right_id_in_orbit=laser_right_id_in_orbit)
            orbit.moving_objects.append(mo)
            # orbit.moving_objects_dict[moving_object_id] = mo
            all_moving_objects.append(mo)
            all_moving_objects_dict[moving_object_id] = mo
            moving_object_id += 1
        horizontal_orbits.append(orbit)
        horizontal_orbits_dict[x] = orbit
        orbit_id += 1

    # Creates vertical orbits and their objects
    for x in range(num_of_orbits_vertical):
        orbit = Orbit(id=orbit_id, id_in_orbit_group=x, is_horizontal=False, x_start=(x+1.0)*(size_x/(num_of_orbits_vertical+1.0))-180.0, y_start=-size_y/2.0, x_end=(x+1.0)*(size_x/(num_of_orbits_vertical+1.0))-180.0, y_end=size_y/2.0-1.0,
                      number_of_objects=num_of_objects_in_orbit_v, moving_object_speed=moving_object_speed)
        for y in range(num_of_objects_in_orbit_v):
            if y == 0:
                laser_left_id = num_of_objects_in_orbit_v + \
                    (num_of_objects_in_orbit_v * orbit_id) - 1
                laser_left_id_in_orbit = num_of_objects_in_orbit_v - 1
                laser_right_id = moving_object_id + 1
                laser_right_id_in_orbit = y+1
            elif y == num_of_objects_in_orbit_v - 1:
                laser_left_id = moving_object_id - 1
                laser_left_id_in_orbit = y-1
                laser_right_id = num_of_objects_in_orbit_v * orbit_id
                laser_right_id_in_orbit = 0
            else:
                laser_left_id = moving_object_id - 1
                laser_left_id_in_orbit = y-1
                laser_right_id = moving_object_id + 1
                laser_right_id_in_orbit = y+1

            mo = MO(
                id=moving_object_id, id_in_orbit=y, orbit_id=orbit_id, is_in_horizontal_orbit=False, x0=(x+1.0)*(size_x/(num_of_orbits_vertical+1.0))-180.0,
                y0=y*(size_y*1.0/num_of_objects_in_orbit_v)-90.0, z0=satellite_altitude, laser_left_id=laser_left_id, laser_left_id_in_orbit=laser_left_id_in_orbit, laser_right_id=laser_right_id, laser_right_id_in_orbit=laser_right_id_in_orbit)
            orbit.moving_objects.append(mo)
            # orbit.moving_objects_dict[moving_object_id] = mo
            all_moving_objects.append(mo)
            all_moving_objects_dict[moving_object_id] = mo
            moving_object_id += 1
        vertical_orbits.append(orbit)
        vertical_orbits_dict[x] = orbit
        orbit_id += 1


# Updates the position of each object in all orbits
def update_moving_object_positions(orbits):
    for orbit in orbits:
        orbit.update_moving_object_positions()


# Updates all distances between all cities and all moving objects
def update_city_moving_object_distances(cities, all_moving_objects):
    for city in cities:
        city.calc_dist_cities_and_moving_objects_angle(
            all_moving_objects, VIEW_ANGLE)
        # print(city.moving_objects_distances_dict)


# Updates all object laser connections
def update_laser_connections(orbits, num_of_orbits_horizontal, num_of_orbits_vertical, all_moving_objects_dict):
    for orbit in orbits:
        orbit.update_laser_connections(
            orbits, num_of_orbits_horizontal, num_of_orbits_vertical)
        orbit.update_laser_distances(all_moving_objects_dict)
