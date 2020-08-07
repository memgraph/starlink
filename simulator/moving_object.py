import simulator.constants as const
import math as m
import simulator.utils as utils


class MovingObject:
    def __init__(self, id, id_in_orbit, orbit_id,  longitude_positions, latitude_positions, altitude, eci_x_positions, eci_y_positions, eci_z_positions, laser_left_id, laser_left_id_in_orbit, laser_right_id, laser_right_id_in_orbit):
        self.id = id
        self.id_in_orbit = id_in_orbit
        self.orbit_id = orbit_id

        self.longitude_positions = longitude_positions
        self.latitude_positions = latitude_positions
        self.altitude = altitude

        self.current_position = 0
        self.positions_lenght = len(longitude_positions) 
        
        self.x = self.longitude_positions[self.current_position]
        self.y = self.latitude_positions[self.current_position]
        self.z = altitude

        self.eci_x_positions = eci_x_positions
        self.eci_y_positions = eci_y_positions
        self.eci_z_positions = eci_z_positions

        self.eci_x = self.eci_x_positions[self.current_position]
        self.eci_y = self.eci_y_positions[self.current_position]
        self.eci_z = self.eci_z_positions[self.current_position]

        self.laser_left_id = laser_left_id
        self.laser_left_id_in_orbit = laser_left_id_in_orbit
        self.laser_right_id = laser_right_id
        self.laser_right_id_in_orbit = laser_right_id_in_orbit

    def updatePosition(self):
        """TODO: remove before deployment"""
        """
        if(utils.eci_distance_coordinates(self.eci_x, self.eci_y, self.eci_z, self.eci_x_positions[self.current_position], self.eci_y_positions[self.current_position], self.eci_z_positions[self.current_position]) < 420):
            print("NOT POSSIBLE")

        if(utils.distance_coordinates(self.x, self.y, self.longitude_positions[self.current_position], self.latitude_positions[self.current_position]) < 3):
            print("NOT POSSIBLE")
            print(utils.distance_coordinates(self.x, self.y,
                                             self.longitude_positions[self.current_position], self.latitude_positions[self.current_position]))
        """

        self.x = self.longitude_positions[self.current_position]
        self.y = self.latitude_positions[self.current_position]

        self.eci_x = self.eci_x_positions[self.current_position]
        self.eci_y = self.eci_y_positions[self.current_position]
        self.eci_z = self.eci_z_positions[self.current_position]

    def update_laser_up(self, orbits_dict):
        if(const.EDGE_CONNECTED or not const.EDGE_CONNECTED and self.orbit_id != 0):
            diff = 100000
            if self.orbit_id == 0:
                laser_up_orbit = const.NUM_ORB - 1
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
                self.laser_up_distance/const.V_LASER_VACUUM

    def update_laser_down(self, orbits_dict):
        if(const.EDGE_CONNECTED or (not const.EDGE_CONNECTED) and self.orbit_id != (const.NUM_ORB - 1)):
            diff = 100000
            if self.orbit_id == const.NUM_ORB - 1:
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
                self.laser_down_distance/const.V_LASER_VACUUM
