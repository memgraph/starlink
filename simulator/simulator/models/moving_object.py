from __future__ import annotations
import os
import math as m
from dataclasses import dataclass, field
from typing import List, Dict, Any


V_LASER_VACUUM = 2.99792458E+8
EDGE_CONNECTED = bool(os.getenv('EDGE_CONNECTED', 'true'))
SAT_PROCESSING_DELAY = float(os.getenv('SAT_PROCESSING_DELAY', 0))


@dataclass
class MovingObject:
    id: int
    id_in_orbit: int

    orbit_id: int
    num_of_orbits: int

    longitude_positions: List
    latitude_positions: List
    elevation_positions: List

    eci_x_positions: List
    eci_y_positions: List
    eci_z_positions: List

    laser_left_id: int
    laser_left_id_in_orbit: int
    laser_right_id: int
    laser_right_id_in_orbit: int

    def __post_init__(self):
        self.current_position = 0
        self.positions_lenght = len(self.longitude_positions)

        self.x = self.latitude_positions[self.current_position]
        self.y = self.longitude_positions[self.current_position]
        self.z = self.elevation_positions[self.current_position]

        self.eci_x = self.eci_x_positions[self.current_position]
        self.eci_y = self.eci_y_positions[self.current_position]
        self.eci_z = self.eci_z_positions[self.current_position]

    def updatePosition(self) -> None:
        self.x = self.latitude_positions[self.current_position]
        self.y = self.longitude_positions[self.current_position]
        self.z = self.elevation_positions[self.current_position]

        self.eci_x = self.eci_x_positions[self.current_position]
        self.eci_y = self.eci_y_positions[self.current_position]
        self.eci_z = self.eci_z_positions[self.current_position]

    def update_laser_up(self, orbits_dict: Dict[int, Any]) -> None:
        if(not EDGE_CONNECTED and self.orbit_id == 0):
            return

        if self.orbit_id == 0:
            laser_up_orbit = self.num_of_orbits - 1
        else:
            laser_up_orbit = self.orbit_id - 1

        diff = 100000
        for moving_object in orbits_dict[laser_up_orbit].moving_objects:
            tmp_diff = MovingObject.eci_distance(self, moving_object)
            if(tmp_diff >= diff):
                continue

            self.laser_up_id = moving_object.id
            self.laser_up_id_in_orbit = moving_object.id_in_orbit
            self.laser_up_orbit_id = moving_object.orbit_id
            self.laser_up_distance = tmp_diff
            diff = tmp_diff

        self.laser_up_transmission_time = 1000 * \
            self.laser_up_distance/V_LASER_VACUUM + SAT_PROCESSING_DELAY

    def update_laser_down(self, orbits_dict: Dict[int, Any]) -> None:
        if(not EDGE_CONNECTED and self.orbit_id == (self.num_of_orbits - 1)):
            return

        if self.orbit_id == self.num_of_orbits - 1:
            laser_down_orbit = 0
        else:
            laser_down_orbit = self.orbit_id + 1

        diff = 100000
        for moving_object in orbits_dict[laser_down_orbit].moving_objects:
            tmp_diff = MovingObject.eci_distance(self, moving_object)
            if (tmp_diff >= diff):
                continue

            self.laser_down_id = moving_object.id
            self.laser_down_id_in_orbit = moving_object.id_in_orbit
            self.laser_down_orbit_id = moving_object.orbit_id
            self.laser_down_distance = tmp_diff
            diff = tmp_diff
        self.laser_down_transmission_time = 1000 * \
            self.laser_down_distance/V_LASER_VACUUM + SAT_PROCESSING_DELAY

    def update_laser_left_right(self, moving_objects_dict_by_id: Dict[id, MovingObject]) -> None:
        self.laser_left_distance = MovingObject.eci_distance(
            self, moving_objects_dict_by_id[self.laser_left_id])

        self.laser_left_transmission_time = 1000*self.laser_left_distance / \
            V_LASER_VACUUM + SAT_PROCESSING_DELAY

        self.laser_right_distance = MovingObject.eci_distance(
            self, moving_objects_dict_by_id[self.laser_right_id])

        self.laser_right_transmission_time = 1000*self.laser_right_distance / \
            V_LASER_VACUUM + SAT_PROCESSING_DELAY

    @staticmethod
    def eci_distance(moving_object_one: MovingObject, moving_object_two: MovingObject) -> float:
        return m.sqrt((moving_object_one.eci_x - moving_object_two.eci_x)**2 +
                      (moving_object_one.eci_y - moving_object_two.eci_y)**2 +
                      (moving_object_one.eci_z - moving_object_two.eci_z)**2)
