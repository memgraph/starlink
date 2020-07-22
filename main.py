from orbit import Orbit as Orbit
from moving_object import MovingObject as MO
import utils
import numpy as np
import matplotlib.pyplot as plt


# initilizes orbits and their objects
def init_orbits_and_objects():
    orbit_id = 0
    moving_object_id = 0

    # create horizontal orbits and their objects
    for x in range(num_of_orbits_horizontal):
        orbit = Orbit(id=orbit_id, id_in_orbit_group=x, is_horizontal=True, x_start=0, y_start=x*(size/num_of_orbits_horizontal), x_end=size-1, y_end=x*(size/num_of_orbits_horizontal),
                      number_of_objects=num_of_objects_in_orbit, moving_object_speed=moving_object_speed)
        for y in range(num_of_objects_in_orbit):
            if y == 0:
                laser_left_id = num_of_objects_in_orbit + \
                    (num_of_objects_in_orbit * x) - 1
                laser_left_id_in_orbit = num_of_objects_in_orbit - 1
                laser_right_id = moving_object_id + 1
                laser_right_id_in_orbit = y+1
            elif y == num_of_objects_in_orbit - 1:
                laser_left_id = moving_object_id - 1
                laser_left_id_in_orbit = y-1
                laser_right_id = num_of_objects_in_orbit * x
                laser_right_id_in_orbit = 0
            else:
                laser_left_id = moving_object_id - 1
                laser_left_id_in_orbit = y-1
                laser_right_id = moving_object_id + 1
                laser_right_id_in_orbit = y+1

            mo = MO(id=moving_object_id, id_in_orbit=y, orbit_id=x, is_in_horizontal_orbit=True, x0=y*(size/num_of_objects_in_orbit),
                    y0=x*(size/num_of_orbits_horizontal), z0=satellite_altitude, laser_left_id=laser_left_id, laser_left_id_in_orbit=laser_left_id_in_orbit, laser_right_id=laser_right_id, laser_right_id_in_orbit=laser_right_id_in_orbit)
            orbit.moving_objects.append(mo)
            # orbit.moving_objects_dict[moving_object_id] = mo
            all_moving_objects.append(mo)
            all_moving_objects_dict[moving_object_id] = mo
            moving_object_id += 1
        horizontal_orbits.append(orbit)
        horizontal_orbits_dict[x] = orbit
        orbit_id += 1

    # create vertical orbits and their objects
    for x in range(num_of_orbits_vertical):
        orbit = Orbit(id=orbit_id, id_in_orbit_group=x, is_horizontal=False, x_start=x*(size/num_of_orbits_horizontal), y_start=0, x_end=x*(size/num_of_orbits_horizontal), y_end=size-1,
                      number_of_objects=num_of_objects_in_orbit, moving_object_speed=moving_object_speed)
        for y in range(num_of_objects_in_orbit):
            if y == 0:
                laser_left_id = num_of_objects_in_orbit + \
                    (num_of_objects_in_orbit * x) - 1
                laser_left_id_in_orbit = num_of_objects_in_orbit - 1
                laser_right_id = moving_object_id + 1
                laser_right_id_in_orbit = y+1
            elif y == num_of_objects_in_orbit - 1:
                laser_left_id = moving_object_id - 1
                laser_left_id_in_orbit = y-1
                laser_right_id = num_of_objects_in_orbit * x
                laser_right_id_in_orbit = 0
            else:
                laser_left_id = moving_object_id - 1
                laser_left_id_in_orbit = y-1
                laser_right_id = moving_object_id + 1
                laser_right_id_in_orbit = y+1

            mo = MO(
                id=moving_object_id, id_in_orbit=y, orbit_id=x, is_in_horizontal_orbit=False, x0=x*(size/num_of_orbits_vertical),
                y0=y*(size/num_of_objects_in_orbit), z0=satellite_altitude, laser_left_id=laser_left_id, laser_left_id_in_orbit=laser_left_id_in_orbit, laser_right_id=laser_right_id, laser_right_id_in_orbit=laser_right_id_in_orbit)
            orbit.moving_objects.append(mo)
            # orbit.moving_objects_dict[moving_object_id] = mo
            all_moving_objects.append(mo)
            all_moving_objects_dict[moving_object_id] = mo
            moving_object_id += 1
        vertical_orbits.append(orbit)
        vertical_orbits_dict[x] = orbit
        orbit_id += 1

# updates the position of each object in all the orbits
def update_moving_object_positions(orbits):
    for orbit in orbits:
        orbit.update_moving_object_positions()

# updates all the object laser connections
def update_laser_connections(orbits):
    for orbit in orbits:
        orbit.update_laser_connections(
            orbits, num_of_orbits_horizontal, num_of_orbits_vertical)
        orbit.update_laser_distances(all_moving_objects_dict)

# updates database entries NOT IMPLEMENTED
def update_memgraph(orbits):
    x = 0


if __name__ == "__main__":
    num_of_orbits_horizontal = 4
    num_of_orbits_vertical = 4
    num_of_objects_in_orbit = 8
    size = 16
    moving_object_speed = 1
    satellite_altitude = 1500
    cities_csv_path = "cities.csv"

    horizontal_orbits = []
    vertical_orbits = []
    all_moving_objects = []
    horizontal_orbits_dict = {}
    vertical_orbits_dict = {}
    all_moving_objects_dict = {}

    init_orbits_and_objects()

    cities = utils.import_cities(cities_csv_path)
    utils.print_cities(cities)

    orbits = (horizontal_orbits + vertical_orbits)

    update_laser_connections(orbits)
    
    """
    # test print
    for x in range(8):
        update_moving_object_positions(orbits)
    utils.print_orbits_and_objects(horizontal_orbits)
    utils.print_laser_connections(horizontal_orbits)
    """
    plt.ion()
    fig = plt.figure(figsize=(8, 8))
    plt.axis([0, size, 0, size])

    while(True):
        update_moving_object_positions(orbits)
        update_laser_connections(orbits)
        update_memgraph(orbits)
        plt.clf()
        plt.draw()
        x = []
        y = []
        for orbit in horizontal_orbits:
            plt.plot([orbit.x_start, orbit.x_end], [orbit.y_start, orbit.y_end])
            for moving_object in orbit.moving_objects:
                x.append(moving_object.x)
                y.append(moving_object.y)
        plt.scatter(x, y)
        fig.canvas.draw_idle()
        plt.pause(1)
    
    plt.waitforbuttonpress()
    
    
    
