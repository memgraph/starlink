from simulator.constants import EDGE_CONNECTED, NUM_ORB, V_LASER_VACUUM, SAT_DELAY
import math as m
from simulator import utils
from dataclasses import dataclass, field
from typing import List


@dataclass
class MovingObject:
    id: int
    id_in_orbit: int
    orbit_id: int

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

    def updatePosition(self):
        self.x = self.latitude_positions[self.current_position]
        self.y = self.longitude_positions[self.current_position]
        self.z = self.elevation_positions[self.current_position]

        self.eci_x = self.eci_x_positions[self.current_position]
        self.eci_y = self.eci_y_positions[self.current_position]
        self.eci_z = self.eci_z_positions[self.current_position]

    def update_laser_up(self, orbits_dict):
        if(EDGE_CONNECTED or not EDGE_CONNECTED and self.orbit_id != 0):
            diff = 100000
            if self.orbit_id == 0:
                laser_up_orbit = NUM_ORB - 1
            else:
                laser_up_orbit = self.orbit_id - 1
            for moving_object in orbits_dict[laser_up_orbit].moving_objects:
                tmp_diff = utils.eci_distance(self, moving_object)
                if (tmp_diff < diff):
                    self.laser_up_id = moving_object.id
                    self.laser_up_id_in_orbit = moving_object.id_in_orbit
                    self.laser_up_orbit_id = moving_object.orbit_id
                    self.laser_up_distance = tmp_diff
                    diff = tmp_diff
            self.laser_up_transmission_time = 1000 * \
                self.laser_up_distance/V_LASER_VACUUM + SAT_DELAY

    def update_laser_down(self, orbits_dict):
        if(EDGE_CONNECTED or (not EDGE_CONNECTED) and self.orbit_id != (NUM_ORB - 1)):
            diff = 100000
            if self.orbit_id == NUM_ORB - 1:
                laser_down_orbit = 0
            else:
                laser_down_orbit = self.orbit_id + 1
            for moving_object in orbits_dict[laser_down_orbit].moving_objects:
                tmp_diff = utils.eci_distance(self, moving_object)
                if (tmp_diff < diff):
                    self.laser_down_id = moving_object.id
                    self.laser_down_id_in_orbit = moving_object.id_in_orbit
                    self.laser_down_orbit_id = moving_object.orbit_id
                    self.laser_down_distance = tmp_diff
                    diff = tmp_diff
            self.laser_down_transmission_time = 1000 * \
                self.laser_down_distance/V_LASER_VACUUM + SAT_DELAY
