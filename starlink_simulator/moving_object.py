import math as m
import starlink_simulator.utils as utils


class MovingObject:
    def __init__(self,
                 id: int,
                 id_in_orbit: int,
                 orbit_id: int,
                 is_in_horizontal_orbit: bool,
                 x0: float,
                 y0: float,
                 z0: float,
                 laser_left_id: int,
                 laser_left_id_in_orbit: int,
                 laser_right_id: int,
                 laser_right_id_in_orbit: int):
        self.id = id
        self.id_in_orbit = id_in_orbit
        self.orbit_id = orbit_id
        self.is_in_horizontal_orbit = is_in_horizontal_orbit

        # Initial position of the object
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0

        # Current position of the object
        self.x = x0
        self.y = y0
        self.z = z0

        # The left and right lasers are connected to objects in the same orbit
        self.laser_left_id = laser_left_id
        self.laser_left_id_in_orbit = laser_left_id_in_orbit
        self.laser_right_id = laser_right_id
        self.laser_right_id_in_orbit = laser_right_id_in_orbit

        # The up and down lasers are connected to objects in neighbouring orbits
        self.laser_up_id = -1   # Global object id
        self.laser_up_id_in_orbit = -1  # Gbject id specific for the orbit
        self.laser_up_orbit_id = -1  # Id of the orbit that contains the object
        self.laser_down_id = -1
        self.laser_down_id_in_orbit = -1
        self.laser_down_orbit_id = -1

        self.laser_left_distance = -1
        self.laser_right_distance = -1
        self.laser_up_distance = -1
        self.laser_down_distance = -1

    def set_laser_up(self,
                     laser_up_id=-1,
                     laser_up_id_in_orbit=-1,
                     laser_up_orbit_id=-1):
        if laser_up_id != -1:
            self.laser_up_id = laser_up_id
        if laser_up_id_in_orbit != -1:
            self.laser_up_id_in_orbit = laser_up_id_in_orbit
        if laser_up_orbit_id != -1:
            self.laser_up_orbit_id = laser_up_orbit_id

    def set_laser_down(self,
                       laser_down_id=-1,
                       laser_down_id_in_orbit=-1,
                       laser_down_orbit_id=-1):
        if laser_down_id != -1:
            self.laser_down_id = laser_down_id
        if laser_down_orbit_id != -1:
            self.laser_down_id_in_orbit = laser_down_id_in_orbit
        if laser_down_orbit_id != -1:
            self.laser_down_orbit_id = laser_down_orbit_id

    def update_laser_up(self,
                        orbits_dict,
                        num_of_orbits_horizontal,
                        num_of_orbits_vertical):
        diff = 100000
        if self.is_in_horizontal_orbit:
            if self.orbit_id == 0:
                laser_up_orbit = num_of_orbits_horizontal - 1
            else:
                laser_up_orbit = self.orbit_id - 1
            for moving_object in orbits_dict[laser_up_orbit].moving_objects:
                tmp_diff = utils.distance(self, moving_object)
                if (tmp_diff < diff):
                    self.laser_up_id = moving_object.id
                    self.laser_up_id_in_orbit = moving_object.id_in_orbit
                    self.laser_up_orbit_id = moving_object.orbit_id
                    self.laser_up_distance = tmp_diff
                    diff = tmp_diff
        else:
            if self.orbit_id == num_of_orbits_horizontal:
                laser_up_orbit = num_of_orbits_horizontal + num_of_orbits_vertical - 1
            else:
                laser_up_orbit = self.orbit_id - 1
            for moving_object in orbits_dict[laser_up_orbit].moving_objects:
                tmp_diff = utils.distance(self, moving_object)
                if (tmp_diff < diff):
                    self.laser_up_id = moving_object.id
                    self.laser_up_id_in_orbit = moving_object.id_in_orbit
                    self.laser_up_orbit_id = moving_object.orbit_id
                    self.laser_up_distance = tmp_diff
                    diff = tmp_diff

    def update_laser_down(self,
                          orbits_dict,
                          num_of_orbits_horizontal,
                          num_of_orbits_vertical):
        diff = 100000
        if self.is_in_horizontal_orbit:
            if self.orbit_id == num_of_orbits_horizontal - 1:
                laser_down_orbit = 0
            else:
                laser_down_orbit = self.orbit_id + 1
            for moving_object in orbits_dict[laser_down_orbit].moving_objects:
                tmp_diff = utils.distance(self, moving_object)
                if (tmp_diff < diff):
                    self.laser_down_id = moving_object.id
                    self.laser_down_id_in_orbit = moving_object.id_in_orbit
                    self.laser_down_orbit_id = moving_object.orbit_id
                    self.laser_down_distance = tmp_diff
                    diff = tmp_diff
        else:
            if self.orbit_id == num_of_orbits_horizontal + num_of_orbits_vertical - 1:
                laser_down_orbit = num_of_orbits_horizontal
            else:
                laser_down_orbit = self.orbit_id + 1
            for moving_object in orbits_dict[laser_down_orbit].moving_objects:
                tmp_diff = utils.distance(self, moving_object)
                if (tmp_diff < diff):
                    self.laser_down_id = moving_object.id
                    self.laser_down_id_in_orbit = moving_object.id_in_orbit
                    self.laser_down_orbit_id = moving_object.orbit_id
                    self.laser_down_distance = tmp_diff
                    diff = tmp_diff
