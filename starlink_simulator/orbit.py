import starlink_simulator.utils as utils


class Orbit:
    def __init__(self, id, id_in_orbit_group, is_horizontal, x_start, y_start, x_end, y_end, number_of_objects, moving_object_speed):
        self.id = id
        self.id_in_orbit_group = id_in_orbit_group
        self.is_horizontal = is_horizontal
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        self.number_of_objects = number_of_objects
        self.moving_object_speed = moving_object_speed
        self.moving_objects = []

    def add_object(self, moving_objects):
        self.moving_objects.append(moving_objects)

    def update_moving_object_positions(self):
        for moving_object in self.moving_objects:
            if self.is_horizontal:
                moving_object.x += self.moving_object_speed
                if moving_object.x >= self.x_end + 1:
                    moving_object.x = self.x_start
            else:
                moving_object.y += self.moving_object_speed
                if moving_object.y >= self.y_end + 1:
                    moving_object.y = self.y_start

    def update_laser_connections(self, orbits, num_of_orbits_horizontal, num_of_orbits_vertical):
        for moving_object in self.moving_objects:
            moving_object.update_laser_up(orbits, num_of_orbits_horizontal, num_of_orbits_vertical)
            moving_object.update_laser_down(orbits, num_of_orbits_horizontal, num_of_orbits_vertical)

    def update_laser_distances(self, all_moving_objects_dict):
        for moving_object in self.moving_objects:
            moving_object.laser_left_distance = utils.distance(moving_object, all_moving_objects_dict[moving_object.laser_left_id])
            moving_object.laser_right_distance = utils.distance(moving_object, all_moving_objects_dict[moving_object.laser_right_id])
