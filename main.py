import utils as utils
import relation_utils as ru
import constants as const
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


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
    scat.set_offsets(np.c_[x, y])
    ax.axis([0, const.SIZE, 0, const.SIZE])
    ax.imshow(img, aspect="auto", extent=(0, const.SIZE, 0, const.SIZE))


def update(frame):
    ru.update_moving_object_positions(orbits)
    ru.update_laser_connections(
        orbits, const.NUM_ORB_H, const.NUM_ORB_V, ru.all_moving_objects)
    ru.update_city_moving_object_distances(cities, ru.all_moving_objects)
    x = []
    y = []
    for orbit in orbits:
        for moving_object in orbit.moving_objects:
            x.append(moving_object.x)
            y.append(moving_object.y)
            if(moving_object.id == 8):
                plot_lines_left.set_data([moving_object.x, ru.all_moving_objects_dict[moving_object.laser_left_id].x], [
                                         moving_object.y, ru.all_moving_objects_dict[moving_object.laser_left_id].y])
                plot_lines_right.set_data([moving_object.x, ru.all_moving_objects_dict[moving_object.laser_right_id].x], [
                                          moving_object.y, ru.all_moving_objects_dict[moving_object.laser_right_id].y])
                plot_lines_up.set_data([moving_object.x, ru.all_moving_objects_dict[moving_object.laser_up_id].x], [
                                       moving_object.y, ru.all_moving_objects_dict[moving_object.laser_up_id].y])
                plot_lines_down.set_data([moving_object.x, ru.all_moving_objects_dict[moving_object.laser_down_id].x], [
                                         moving_object.y, ru.all_moving_objects_dict[moving_object.laser_down_id].y])
    scat.set_offsets(np.c_[x, y])


if __name__ == "__main__":

    """
    db = Memgraph()
    db_operations.clear(db)
    """

    ru.init_orbits_and_objects(const.NUM_ORB_H, const.NUM_ORB_V,
                               const.NUM_OBJ_ORB, const.SIZE, const.SPEED, const.SAT_ALT)

    cities_csv_path = "cities.csv"
    cities = utils.import_cities(cities_csv_path)
    ru.update_city_moving_object_distances(cities, ru.all_moving_objects)

    orbits = (ru.horizontal_orbits + ru.vertical_orbits)
    ru.update_laser_connections(
        orbits, const.NUM_ORB_H, const.NUM_ORB_V, ru.all_moving_objects)

    utils.assign_speed(const.SIZE, ru.horizontal_orbits)

    """
    db_operations.create_moving_objects(db, ru.all_moving_objects)
    db_operations.create_cities(db, cities)
    db_operations.create_city_moving_objects_visibility(
        db, cities, ru.all_moving_objects)
    db_operations.create_laser_connections(db, ru.all_moving_objects)
    """

    fig, ax = plt.subplots()
    img = plt.imread(".\map.jpg")
    orbit_lines = []
    plot_lines_left, = ax.plot([], [])
    plot_lines_right, = ax.plot([], [])
    plot_lines_up, = ax.plot([], [])
    plot_lines_down, = ax.plot([], [])
    scat = ax.scatter([], [])
    x = []
    y = []
    ani = animation.FuncAnimation(
        fig, update, interval=1000, init_func=setup_plot)
    plt.show()

    """
    while(True):
        update_moving_object_positions(orbits)
        update_laser_connections(orbits, num_of_orbits_horizontal, num_of_orbits_vertical)
        #db_operations.update_object_positions(db, all_moving_objects)
        #db_operations.update_laser_connections(db, all_moving_objects)
        time.sleep(20)
    """
