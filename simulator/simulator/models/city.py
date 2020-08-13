from simulator.constants import VIEW_ANGLE, V_RADIO, RELAY_DELAY
from simulator.models.stationary_object import StationaryObject
from simulator import utils
from skyfield.api import Topos
import csv


class City(StationaryObject):
    def __init__(self, id, x, y, z, eci_x_positions, eci_y_positions, eci_z_positions, name):
        StationaryObject.__init__(
            self, id, x, y, z, eci_x_positions, eci_y_positions, eci_z_positions)
        self.name = name
        self.id = id
        self.moving_objects_distances_dict = {}
        self.moving_objects_tt_dict = {}

    def city_visible_moving_object_distances(self, moving_objects_dict_by_id):
        self.moving_objects_distances_dict = {}
        self.moving_objects_tt_dict = {}
        for moving_object_id in moving_objects_dict_by_id.keys():
            angle = utils.calculate_angle(
                self, moving_objects_dict_by_id[moving_object_id])
            if angle <= VIEW_ANGLE:
                dist = utils.eci_distance(
                    self, moving_objects_dict_by_id[moving_object_id])
                self.moving_objects_distances_dict[moving_object_id] = dist
                self.moving_objects_tt_dict[moving_object_id] = dist * \
                    1000/V_RADIO + RELAY_DELAY

    @staticmethod
    def generate_cities(file_path, time):
        cities = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                topos = Topos(latitude_degrees=float(row['latitude']), longitude_degrees=float(
                    row['longitude']), elevation_m=float(row['altitude']))
                geocentric = topos.at(time)
                city = City(id=row['id'], x=topos.latitude.degrees, y=topos.longitude.degrees, z=topos.elevation.km,
                            eci_x_positions=geocentric.position.km[0], eci_y_positions=geocentric.position.km[1], eci_z_positions=geocentric.position.km[2], name=row['name'])
                cities.append(city)
        return cities
