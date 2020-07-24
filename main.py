from orbit import Orbit as Orbit
from moving_object import MovingObject as MO
import utils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


horizontal_orbits = []
vertical_orbits = []
orbits = []
all_moving_objects = []
horizontal_orbits_dict = {}
vertical_orbits_dict = {}
all_moving_objects_dict = {}
x = []
y = []

# initilizes orbits and their objects
def init_orbits_and_objects(num_of_orbits_horizontal, num_of_orbits_vertical, num_of_objects_in_orbit, size, moving_object_speed, satellite_altitude):
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

            mo = MO(id=moving_object_id, id_in_orbit=y, orbit_id=orbit_id, is_in_horizontal_orbit=True, x0=y*(size/num_of_objects_in_orbit),
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
                    (num_of_objects_in_orbit * orbit_id) - 1
                laser_left_id_in_orbit = num_of_objects_in_orbit - 1
                laser_right_id = moving_object_id + 1
                laser_right_id_in_orbit = y+1
            elif y == num_of_objects_in_orbit - 1:
                laser_left_id = moving_object_id - 1
                laser_left_id_in_orbit = y-1
                laser_right_id = num_of_objects_in_orbit * orbit_id
                laser_right_id_in_orbit = 0
            else:
                laser_left_id = moving_object_id - 1
                laser_left_id_in_orbit = y-1
                laser_right_id = moving_object_id + 1
                laser_right_id_in_orbit = y+1

            mo = MO(
                id=moving_object_id, id_in_orbit=y, orbit_id=orbit_id, is_in_horizontal_orbit=False, x0=x*(size/num_of_orbits_vertical),
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
def update_laser_connections(orbits, num_of_orbits_horizontal, num_of_orbits_vertical):
    for orbit in orbits:
        orbit.update_laser_connections(
            orbits, num_of_orbits_horizontal, num_of_orbits_vertical)
        orbit.update_laser_distances(all_moving_objects_dict)


def setup_plot():
    for orbit in orbits:
        if orbit.is_horizontal:
            orbit_lines.append(
                plt.plot([orbit.x_start, orbit.x_end+1], [orbit.y_start, orbit.y_end]))
        else:
            orbit_lines.append(plt.plot([orbit.x_start, orbit.x_end], [
                               orbit.y_start, orbit.y_end+1]))
        for moving_object in orbit.moving_objects:
            x.append(moving_object.x)
            y.append(moving_object.y)
    # scat.set_data(ax.scatter(x, y, vmin=0, vmax=1, c='#ff7f0e', edgecolor="k"))
    scat.set_offsets(np.c_[x, y])
    ax.axis([0, size, 0, size])
    ax.imshow(img, aspect="auto", extent=(0, size, 0, size))


def update(frame):
    update_moving_object_positions(orbits)
    update_laser_connections(
        orbits, num_of_orbits_horizontal, num_of_orbits_vertical)
    x = []
    y = []
    for orbit in orbits:
        for moving_object in orbit.moving_objects:
            x.append(moving_object.x)
            y.append(moving_object.y)
            if(moving_object.id == 8):
                plot_lines_left.set_data([moving_object.x, all_moving_objects_dict[moving_object.laser_left_id].x], [
                                         moving_object.y, all_moving_objects_dict[moving_object.laser_left_id].y])
                plot_lines_right.set_data([moving_object.x, all_moving_objects_dict[moving_object.laser_right_id].x], [
                                          moving_object.y, all_moving_objects_dict[moving_object.laser_right_id].y])
                plot_lines_up.set_data([moving_object.x, all_moving_objects_dict[moving_object.laser_up_id].x], [
                                       moving_object.y, all_moving_objects_dict[moving_object.laser_up_id].y])
                plot_lines_down.set_data([moving_object.x, all_moving_objects_dict[moving_object.laser_down_id].x], [
                                         moving_object.y, all_moving_objects_dict[moving_object.laser_down_id].y])

    # scat.set_data(ax.scatter(x, y, vmin=0, vmax=1, c='#ff7f0e', edgecolor="k"))
    scat.set_offsets(np.c_[x, y])


if __name__ == "__main__":
    num_of_orbits_horizontal = 5
    num_of_orbits_vertical = 5
    num_of_objects_in_orbit = 4
    size = 15
    moving_object_speed = 1
    satellite_altitude = 1500
    cities_csv_path = "cities.csv"

    #db = Memgraph()
    # db_operations.clear(db)

    init_orbits_and_objects(num_of_orbits_horizontal, num_of_orbits_vertical,
                            num_of_objects_in_orbit, size, moving_object_speed, satellite_altitude)

    cities = utils.import_cities(cities_csv_path)
    # utils.print_cities(cities)

    orbits = (horizontal_orbits + vertical_orbits)

    update_laser_connections(
        orbits, num_of_orbits_horizontal, num_of_orbits_vertical)

    utils.assign_speed(size, horizontal_orbits)
    #db_operations.create_moving_objects(db, all_moving_objects)
    #db_operations.create_cities(db, cities)
    #db_operations.create_laser_connections(db, all_moving_objects)
    # utils.print_laser_connections(orbits)

    fig, ax = plt.subplots()
    img = plt.imread(".\map.jpg")
    orbit_lines = []
    plot_lines_left, = ax.plot([], [])
    plot_lines_right, = ax.plot([], [])
    plot_lines_up, = ax.plot([], [])
    plot_lines_down, = ax.plot([], [])
    scat = ax.scatter([], [])

    ani = animation.FuncAnimation(
        fig, update, interval=2000, init_func=setup_plot)
    plt.show()

    """
    while(True):
        update_moving_object_positions(orbits)
        update_laser_connections(orbits, num_of_orbits_horizontal, num_of_orbits_vertical)
        #db_operations.update_object_positions(db, all_moving_objects)
        #db_operations.update_laser_connections(db, all_moving_objects)
        time.sleep(20)
    """
