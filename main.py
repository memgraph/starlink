from orbit import Orbit as Orbit
from moving_object import MovingObject as MO


# initilizes orbits and their objects
def init_orbits_and_objects():
    orbit_id = 0
    moving_object_id = 0

    # create horizontal orbits and their objects
    for x in range(num_of_orbits_horizontal):
        orbit = Orbit(id=orbit_id, id_in_orbit_group=x, is_horizontal=True, starting_point=0, ending_point=size-1,
                      number_of_objects=num_of_objects_in_orbit, moving_object_speed=moving_object_speed)
        for y in range(num_of_objects_in_orbit):
            if y == 0:
                laser_left_id = num_of_objects_in_orbit-1
                laser_rigth_id = 1
            elif y == num_of_objects_in_orbit - 1:
                laser_left_id = num_of_objects_in_orbit - 2
                laser_rigth_id = 0
            else:
                laser_left_id = y-1
                laser_rigth_id = y+1

            mo = MO(id=moving_object_id, id_in_orbit=y, orbit_id=x, is_in_horizontal_orbit=True, x0=y*(size/num_of_orbits_horizontal),
                y0=x*(size/num_of_orbits_horizontal), laser_left_id=laser_left_id, laser_right_id=laser_rigth_id)
            orbit.moving_objects.append(mo)
            all_moving_objects.append(mo)
            moving_object_id += 1
        horizontal_orbits.append(orbit)
        horizontal_orbits_dict[x] = orbit
        orbit_id += 1

    # create vertical orbits and their objects
    for x in range(num_of_orbits_vertical):
        orbit = Orbit(id=orbit_id, id_in_orbit_group=x, is_horizontal=False, starting_point=0, ending_point=size-1,
                      number_of_objects=num_of_objects_in_orbit, moving_object_speed=moving_object_speed)
        for y in range(num_of_objects_in_orbit):
            if y == 0:
                laser_left_id = num_of_objects_in_orbit-1
                laser_rigth_id = 1
            elif y == num_of_objects_in_orbit-1:
                laser_left_id = num_of_objects_in_orbit-2
                laser_rigth_id = 0
            else:
                laser_left_id = y-1
                laser_rigth_id = y+1

            mo = MO(
                id=moving_object_id, id_in_orbit=y, orbit_id=x, is_in_horizontal_orbit=False, x0=x*(size/num_of_orbits_vertical),
                y0=y*(size/num_of_orbits_vertical), laser_left_id=laser_left_id, laser_right_id=laser_rigth_id)
            orbit.moving_objects.append(mo)
            all_moving_objects.append(mo)
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
        orbit.update_laser_connections(orbits, num_of_orbits_horizontal, num_of_orbits_vertical)

# updates database entries NOT IMPLEMENTED
def update_memgraph(orbits):
    x = 0

# prints the coordinates of all the objects in the orbits
def print_orbits_and_objects(orbits):
    for i in orbits:
        for j in i.moving_objects:
            print("Orbit: ", i.id, "  Object: (", j.x, ", ", j.y, ")")

# prints the indexes of all the laser connections of objects in the orbits
def print_laser_connections(orbits):
    for i in orbits:
        for j in i.moving_objects:
            print("Orbit: ", i.id, "  Object: ", j.id, " (", j.x, ", ", j.y, ")  Laser left: (", j.laser_left_id, ")  Laser right: (", j.laser_right_id, ")  Laser up: (", j.laser_up_id, ")  Laser down: (", j.laser_down_id, ")")


if __name__ == "__main__":
    num_of_orbits_horizontal = 4
    num_of_orbits_vertical = 4
    num_of_objects_in_orbit = 4
    size = 16
    moving_object_speed = 1

    horizontal_orbits = []
    vertical_orbits = []
    all_moving_objects = []
    horizontal_orbits_dict = {}
    vertical_orbits_dict = {}

    init_orbits_and_objects()

    orbits = (horizontal_orbits + vertical_orbits)

    update_laser_connections(orbits)
    
    # test print
    for x in range(0):
        update_moving_object_positions(orbits)
    print_orbits_and_objects(horizontal_orbits)
    print_laser_connections(horizontal_orbits)

    """
    while(True):
        update_moving_object_positions(orbits)
        update_laser_connections(orbits)
        update_memgraph(orbits)
    """
