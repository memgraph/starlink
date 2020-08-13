import os
from dataclasses import dataclass, field
from simulator import utils
from typing import List


V_LASER_VACUUM = 2.99792458E+8
SAT_PROCESSING_DELAY = float(os.getenv('SAT_PROCESSING_DELAY', 0))


@dataclass
class Orbit:
    id: int

    def __post_init__(self):
        self.moving_objects = []

    def add_object(self, moving_objects):
        self.moving_objects.append(moving_objects)

    def update_moving_object_positions(self):
        for moving_object in self.moving_objects:
            moving_object.current_position += 1
            if (moving_object.current_position == moving_object.positions_lenght):
                moving_object.current_position = 0

            moving_object.updatePosition()

    def update_laser_connections(self, orbits_dict_by_id):
        for moving_object in self.moving_objects:
            moving_object.update_laser_up(orbits_dict_by_id)
            moving_object.update_laser_down(orbits_dict_by_id)

    def update_laser_distances(self, moving_objects_dict_by_id):
        for moving_object in self.moving_objects:
            moving_object.laser_left_distance = utils.eci_distance(
                moving_object, moving_objects_dict_by_id[moving_object.laser_left_id])
            moving_object.laser_left_transmission_time = 1000*moving_object.laser_left_distance / \
                V_LASER_VACUUM + SAT_PROCESSING_DELAY
            moving_object.laser_right_distance = utils.eci_distance(
                moving_object, moving_objects_dict_by_id[moving_object.laser_right_id])
            moving_object.laser_right_transmission_time = 1000*moving_object.laser_right_distance / \
                V_LASER_VACUUM + SAT_PROCESSING_DELAY
