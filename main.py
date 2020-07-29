import constants as const
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import orbital_mechanics_utils
import relation_utils
import utils


def setup_plot():
    for orbit in orbits:
        for moving_object in orbit.moving_objects:
            x.append(moving_object.x)
            y.append(moving_object.y)
    scat.set_offsets(np.c_[x, y])
    ax.axis([-const.SIZE_X/2, const.SIZE_X/2, -const.SIZE_Y/2, const.SIZE_Y/2])
    ax.imshow(img, aspect="auto", extent=(-const.SIZE_X/2,
                                          const.SIZE_X/2, -const.SIZE_Y/2, const.SIZE_Y/2))
    for city in cities:
        plt.scatter(city.x, city.y)


def update(frame):
    relation_utils.update_all_positions_and_relations(
        cities, orbits, orbits_dict, moving_objects, moving_objects_dict)
   
    x = []
    y = []
    for orbit in orbits:
        for moving_object in orbit.moving_objects:
            x.append(moving_object.x)
            y.append(moving_object.y)
            if moving_object.id == 60:
                plot_lines_left.set_data([moving_object.x, moving_objects_dict[moving_object.laser_left_id].x], [
                    moving_object.y, moving_objects_dict[moving_object.laser_left_id].y])
                plot_lines_right.set_data([moving_object.x, moving_objects_dict[moving_object.laser_right_id].x], [
                    moving_object.y, moving_objects_dict[moving_object.laser_right_id].y])
                plot_lines_up.set_data([moving_object.x, moving_objects_dict[moving_object.laser_up_id].x], [
                                       moving_object.y, moving_objects_dict[moving_object.laser_up_id].y])
                plot_lines_down.set_data([moving_object.x, moving_objects_dict[moving_object.laser_down_id].x], [
                                         moving_object.y, moving_objects_dict[moving_object.laser_down_id].y])
                #print(moving_object.eci_x, " - ", moving_object.eci_y, " - ", moving_object.eci_z)
    scat.set_offsets(np.c_[x, y])


if __name__ == "__main__":

    """
    db = Memgraph()
    db_operations.clear(db)
    """

    orbits, orbits_dict, moving_objects, moving_objects_dict = orbital_mechanics_utils.generateMovingObjects()

    cities_csv_path = "cities.csv"
    cities = orbital_mechanics_utils.import_cities(cities_csv_path)

    relation_utils.update_city_moving_object_distances(cities, moving_objects)
    relation_utils.update_laser_connections(
        orbits, orbits_dict, moving_objects_dict)

    """
    db_operations.create_moving_objects(db, ru.all_moving_objects)
    db_operations.create_cities(db, cities)
    db_operations.create_city_moving_objects_visibility(
        db, cities, ru.all_moving_objects)
    db_operations.create_laser_connections(db, ru.all_moving_objects)
    """

    fig, ax = plt.subplots()
    img = plt.imread(".\map.jpg")
    scat = ax.scatter([], [])

    x = []
    y = []
    plot_lines_left, = ax.plot([], [])
    plot_lines_right, = ax.plot([], [])
    plot_lines_up, = ax.plot([], [])
    plot_lines_down, = ax.plot([], [])

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
