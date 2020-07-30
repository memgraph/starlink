import starlink_simulator.constants as const
from starlink_simulator.stationary_object import StationaryObject
import starlink_simulator.utils as utils


class City(StationaryObject):
    def __init__(self, id, x, y, z, eci_x_positions, eci_y_positions, eci_z_positions, name):
        StationaryObject.__init__(
            self, id, x, y, z, eci_x_positions, eci_y_positions, eci_z_positions)
        self.name = name
        self.id = id
        self.moving_objects_distances_dict = {}
        self.moving_objects_tt_dict = {}


    # Calculates distances between cities and moving objects in view_angle field of view
    def city_visible_moving_object_distances(self, moving_objects):
        for moving_object in moving_objects:
            angle = utils.calculate_angle(self, moving_object)
            if angle <= const.VIEW_ANGLE:
                dist = utils.eci_distance(self, moving_object)
                self.moving_objects_distances_dict[moving_object.id] = dist
            self.moving_objects_tt_dict[moving_object.id] = dist*1000/const.V_RADIO
