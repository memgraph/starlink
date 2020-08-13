from simulator.constants import VIEW_ANGLE, V_RADIO, RELAY_DELAY
from simulator.models.stationary_object import StationaryObject
from simulator import utils
from skyfield.api import Topos
from pathlib import Path
import csv
from dataclasses import dataclass, field
from typing import List
import math


@dataclass
class City(StationaryObject):
    name: str

    def __post_init__(self):
        StationaryObject.__post_init__(self)
        self.moving_objects_distances_dict = {}
        self.moving_objects_tt_dict = {}

    def city_visible_moving_object_distances(self, moving_objects_dict_by_id):
        self.moving_objects_distances_dict = {}
        self.moving_objects_tt_dict = {}
        for moving_object_id in moving_objects_dict_by_id.keys():
            angle = City.calculate_angle(
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
        path = Path(__file__).parent.parent.parent / file_path
        with path.open() as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:

                topos = Topos(latitude_degrees=float(row['latitude']),
                              longitude_degrees=float(row['longitude']),
                              elevation_m=float(row['altitude']))

                geocentric = topos.at(time)

                city = City(id=row['id'],
                            x=topos.latitude.degrees,
                            y=topos.longitude.degrees,
                            z=topos.elevation.km,
                            eci_x_positions=geocentric.position.km[0],
                            eci_y_positions=geocentric.position.km[1],
                            eci_z_positions=geocentric.position.km[2],
                            name=row['name'])

                cities.append(city)
        return cities

    @staticmethod
    def calculate_angle(city, moving_object):
        angle = math.acos(
            moving_object.z / utils.eci_distance(moving_object, city)) * 180.0/math.pi
        return angle
