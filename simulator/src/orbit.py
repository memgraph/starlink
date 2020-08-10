import src.constants as const
import src.utils as utils


class Orbit:
    def __init__(self, id):
        self.id = id
        self.moving_objects = []

    def add_object(self, moving_objects):
        self.moving_objects.append(moving_objects)

    def update_moving_object_positions(self):
        for moving_object in self.moving_objects:
            moving_object.current_position += 1
            if (moving_object.current_position == moving_object.positions_lenght):
                moving_object.current_position = 0

            moving_object.updatePosition()

    def update_laser_connections(self, moving_objects):
        for moving_object in self.moving_objects:
            moving_object.update_laser_up(moving_objects)
            moving_object.update_laser_down(moving_objects)

    def update_laser_distances(self, moving_objects_dict):
        for moving_object in self.moving_objects:
            moving_object.laser_left_distance = utils.eci_distance(
                moving_object, moving_objects_dict[moving_object.laser_left_id])
            moving_object.laser_left_transmission_time = 1000*moving_object.laser_left_distance / \
                const.V_LASER_VACUUM + const.SAT_DELAY
            moving_object.laser_right_distance = utils.eci_distance(
                moving_object, moving_objects_dict[moving_object.laser_right_id])
            moving_object.laser_right_transmission_time = 1000*moving_object.laser_right_distance / \
                const.V_LASER_VACUUM + const.SAT_DELAY
